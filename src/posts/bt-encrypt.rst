==================================
The BitTorrent Encryption Protocol
==================================

:Date: 2023-10-19
:Category: Software
:Tags: BitTorrent, encryption
:Summary:
    The `encryption protocol`_ used by the BitTorrent_ peer-to-peer
    file-sharing protocol — known variously as Message Stream Encryption (MSE),
    Protocol Encryption (PE), or MSE/PE, among other names — is what keeps you
    secure while you download massive amounts of … Linux ISOs.  Here's how it
    works.

The `encryption protocol`_ used by the BitTorrent_ peer-to-peer file-sharing
protocol — known variously as Message Stream Encryption (MSE), Protocol
Encryption (PE), or MSE/PE, among other names — is what keeps you secure while
you download massive amounts of … Linux ISOs.  While some (including the
creator of BitTorrent) have been critical of the protocol, comparing it to mere
"obfuscation," it remains highly popular among users distributing perfectly
legitimate files over the internet that ISPs shouldn't concern themselves
about.

The *de facto* official specification for the protocol appears to be
<https://wiki.vuze.com/w/Message_Stream_Encryption>, but the page has been down
whenever I've checked recently, and the actual content is not optimally
presented.  Thus, I've written up everything I've been able to determine about
MSE/PE here.

.. _encryption protocol: https://en.wikipedia.org/wiki/BitTorrent_protocol_encryption
.. _BitTorrent: https://en.wikipedia.org/wiki/BitTorrent


.. contents::

Overview
========

An MSE/PE connection begins with the client and server performing a
`Diffie–Hellman key exchange <DH_>`_ handshake, in which both parties generate
a pair of public & private keys and then exchange their public keys, after
which — by the power of mathematics — they independently calculate the same
number (the *shared secret*), which remains unknown to eavesdroppers.  Each
party then uses the shared secret to initialize two keystreams_: infinite
generators of pseudo-random bytes calculated from an initial value; the bytes
from one keystream are then used to encrypt & decrypt data sent from the client
to the server, and the other keystream is used for data sent from the server to
the client.

After the handshake, the parties transmit their data, which is encrypted using
a method negotiated during the handshake; the only defined options are to keep
using the keystreams or to stop using encryption entirely.

.. _DH: https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange
.. _keystreams: https://en.wikipedia.org/wiki/Keystream
.. _stream ciphers: https://en.wikipedia.org/wiki/Stream_cipher


Definitions
===========

MSE/PE encryption uses the following constants and functions:

- ``P`` is the following 96-byte (768-bit) prime, rendered in hexadecimal::

    ffffffffffffffff c90fdaa22168c234  c4c6628b80dc1cd1 29024e088a67cc74
    020bbea63b139b22 514a08798e3404dd  ef9519b3cd3a431b 302b0a6df25f1437
    4fe1356d6d51c245 e485b576625e7ec6  f44c42e9a63a3621 0000000000090563

- ``G`` is 2 (a `primitive root`_ *modulo* ``P``).

- ``SKEY`` is a shared key — a byte string with a value known or recognizable
  by both parties.  For BitTorrent, this is the 20-byte info hash of the
  torrent the connection is dedicated to.

- ``len(X)`` is the length of the byte string ``X`` as a two-byte big-endian
  integer.  The length of ``X`` cannot exceed 65535.

- ``HASH(X)`` is the 20-byte SHA1 hash of the byte string ``X``.

.. _primitive root: https://en.wikipedia.org/wiki/Primitive_root_modulo_n


Client's Handshake
==================

The peer initiating an MSE/PE connection performs its side of the handshake as
follows as soon as it opens the connection:

- The client generates a random integer ``Xa`` to use as its private key for
  this connection only.  ``Xa`` must be at least 128 bits long; using more than
  180 bits is not believed to add further security.  160 bits is recommended.

- The client calculates its public key: ``Ya = pow(G, Xa) mod P``.

- The client sends packet 1: ``Ya`` encoded as a 96-byte (768-bit) big-endian
  integer, followed by a string of random bytes with a randomly-chosen length
  from 0 to 512.

- The client receives packet 2.  Because the length of this packet is not known
  by the client and there is no means for indicating the end of the packet, the
  client must identify the end of the packet by waiting for sufficient time
  (the original spec says 30 seconds) for the entire packet to arrive.  If the
  server sends fewer than 96 bytes in that time (For comparison, the
  unencrypted BitTorrent handshake message is 68 bytes), or the server sends
  more than 608 bytes, then the server is not performing a valid MSE/PE
  handshake.

- The client extracts ``Yb`` from the first 96 bytes of packet 2 and computes
  the Diffie-Hellman shared secret: ``S = pow(Yb, Xa) mod P``.  ``Xa`` is then
  securely discarded.

  - When used as a byte string in later steps, ``S`` is encoded as a 96-byte
    (768-bit) big-endian integer.

- The client initializes an outgoing `RC4 <https://en.wikipedia.org/wiki/RC4>`_
  keystream from the key ``HASH("keyA" + S + SKEY)`` and an incoming RC4
  keystream from the key ``HASH("keyB" + S + SKEY)``.  The first 1024 bytes
  output by each keystream are discarded.

- The client sends packet 3, constructed as follows::

        HASH("req1" + S)
        + (HASH("req2" + SKEY) XOR HASH("req3" + S))
        + RC4(VC + crypto_provide + len(PadC) + PadC + len(IA) + IA)

  where:

  - ``RC4(X)`` encrypts the byte string ``X`` by XORing it with bytes produced
    by the outgoing RC4 keystream.

  - ``VC`` is a verification constant of eight zero-valued bytes that is used
    to verify whether the other party knows ``S`` and ``SKEY`` and thus defeat
    replay attacks of the ``SKEY`` hash.

  - ``crypto_provide`` is a 32-bit big-endian integer in which individual bits
    are set to indicate the encryption methods supported by the client.  The
    defined methods are plain text (bit 0x01) and RC4 (bit 0x02).

  - ``PadC`` is arbitrary data with a length of 0 to 512 bytes, reserved for
    extending the crypto handshake in future versions.  Current implementations
    may choose to set it to the empty string.  For padding-only usage in the
    current version, the bytes should be zeroed.

  - ``IA`` is the initial (post-handshake) data that the client wishes to send.
    It may be 0 bytes long, and it cannot be more than 65535 bytes long.

- The client receives & verifies packet 4:

  - The first eight bytes are received and decrypted by XORing them with bytes
    from the incoming RC4 keystream.  If the resulting bytes are not all zero,
    the handshake is invalid.

  - The next four bytes are received and decrypted in the same manner to obtain
    ``crypto_select``, a big-endian integer in which a bit corresponding to one
    of the methods given in ``crypto_provide`` has been set in order to
    indicate which encryption method will be used after the handshake.  If
    ``crypto_select`` does not have exactly one bit set, or if the set bit does
    not correspond to one of the methods in ``crypto_provide``, the handshake
    is invalid.

  - The next two bytes are received and decrypted to obtain ``len(PadD)``.

  - The next ``len(PadD)`` bytes are received and decrypted to obtain ``PadD``.
    Note that, although the result of the decryption is unused, the decryption
    must still be performed in order to keep the incoming keystream in sync
    with the server's outgoing keystream.


Server's Handshake
==================

The peer receiving an MSE/PE connection performs its side of the handshake as
follows as soon as it accepts the connection:

- The server generates a private key ``Xb`` following the same rules as for the
  client's private key.

- The server calculates its public key: ``Yb = pow(G, Xb) mod P``.

- The server sends packet 2: ``Yb`` encoded as a 96-byte (768-bit) big-endian
  integer, followed by a string of random bytes with a randomly-chosen length
  from 0 to 512.

- The server receives packet 1.  As with the client's receipt of packet 2, the
  server must determine the end of packet 1 by waiting for sufficient time (the
  original spec says 30 seconds) for the entire packet to arrive.

- The server extracts ``Ya`` from the first 96 bytes of packet 1 and computes
  the Diffie-Hellman shared secret: ``S = pow(Ya, Xb) mod P`` (This is equal to
  the ``S`` computed by the client).  ``Xb`` is then securely discarded.

  - When used as a byte string in later steps, ``S`` is encoded as a 96-byte
    (768-bit) big-endian integer.

- The server receives & verifies packet 3:

  - The first 20 bytes must equal ``HASH("req1" + S)``.

  - The next 20 bytes are received and XORed with ``HASH("req3" + S)`` to
    obtain ``HASH("req2" + SKEY)``.  The server then identifies ``SKEY`` by
    comparing this hash against ``HASH("req2" + K)`` for all known/accepted
    shared keys ``K``.  (For BitTorrent, this means comparing against
    ``HASH("req2" + info_hash)`` for all info hashes of torrents managed by the
    server.)

  - The server initializes an outgoing RC4 keystream from the key ``HASH("keyB"
    + S + SKEY)`` and an incoming RC4 keystream from the key ``HASH("keyA" + S
    + SKEY)``.  (Note that this is the reverse of the client.)  The first 1024
    bytes output by each keystream are discarded.

  - The next eight bytes are received and decrypted by XORing them with bytes
    from the incoming RC4 keystream.  If the resulting bytes are not all zero,
    the handshake is invalid.

  - The next four bytes are received and decrypted in the same manner to obtain
    ``crypto_provide``.

  - The next two bytes are received and decrypted to obtain ``len(PadC)``.

  - The next ``len(PadC)`` bytes are received and decrypted to obtain ``PadC``.
    Note that, although the result of the decryption is unused, the decryption
    must still be performed in order to keep the incoming keystream in sync
    with the client's outgoing keystream.

  - The next two bytes are received and decrypted to obtain ``len(IA)``.

  - The next ``len(IA)`` bytes are received and decrypted to obtain ``IA``, the
    beginning of the actual data being transferred.

- The server chooses one of the encryption methods given by ``crypto_provide``
  to use for the rest of the connection.  Bits with unknown meanings are
  ignored.  If ``crypto_provide`` does not contain any encryption methods that
  the server supports, the handshake fails.

- The server sends packet 4: ``RC4(VC + crypto_select + len(PadD) + PadD)``,
  where:

  - ``RC4(X)`` encrypts the byte string ``X`` by XORing it with bytes produced
    by the server's outgoing RC4 keystream.

  - ``VC`` is eight zero-valued bytes, the same as in packet 3.

  - ``crypto_select`` is a 32-bit big-endian integer with one bit set to
    indicate the encryption method chosen by the server.  The bits have the
    same meanings as for ``crypto_provide``.

  - ``PadD`` is arbitrary data with a length of 0 to 512 bytes, reserved for
    extending the crypto handshake in future versions.  Current implementations
    may choose to set them to 0-length.  For padding-only usage in the current
    version, they should be zeroed.


After the Handshake
===================

Once all of the above is carried out, the MSE/PE handshake is complete, and the
client & server transmit the data they came here to transmit, encrypted using
the selected encryption method.  If plain text was selected, further data is
sent & received as-is without encryption.  If RC4 was selected, sent & received
data will be encrypted using the sender's outgoing RC4 keystream and decrypted
using the receiver's incoming RC4 keystream; these are the same keystreams as
used during the handshake, i.e., they are not reinitialized.


BitTorrent-Specific Aspects
===========================

Detecting Encryption
--------------------

MSE/PE was introduced into a world where BitTorrent connections were already
being made without encryption, and many connections still aren't encrypted, so
peers need a way to determine whether a fresh connection is encrypted or not.

When a BitTorrent peer that supports MSE/PE receives an incoming connection, it
can determine whether an MSE/PE handshake is being performed by checking
whether the first 20 bytes received equal the BitTorrent handshake header
``"\x13BitTorrent protocol"``; if the bytes match, the connection is (almost
certainly) not using MSE/PE, and the peer can choose to either continue the
connection unencrypted or else sever the connection.

When a BitTorrent peer that supports MSE/PE makes an outgoing connection, it
has the following options, which it chooses among based on its configuration
and any broadcasts of encryption support it's received (see below):

- The peer can attempt an MSE/PE handshake; if that fails, it abandons the
  remote peer.

- The peer can attempt an MSE/PE handshake; if that fails, it severs the
  connection and tries to reconnect without using encryption.

- The peer connects without using encryption.  If the remote peer sends a `BEP
  10`_ extended handshake containing an ``e`` value of ``1``, the local peer
  severs the connection and reconnects using MSE/PE.

- The peer connects without using encryption and does not use MSE/PE with the
  remote peer.


Broadcasting Encryption Support
-------------------------------

BitTorrent peers can broadcast their support of MSE/PE to other peers via HTTP
trackers and/or Peer Exchange.  (The UDP tracker protocol and DHT do not appear
to have any capabilities for broadcasting encryption support.)

When a BitTorrent peer that supports MSE/PE makes an announcement to an HTTP
tracker, it can include one or more of the following URL query parameters:

- ``supportcrypto=1`` — Indicates that the peer can create & receive MSE/PE
  connections

- ``requirecrypto=1`` — Indicates that the peer only creates & accepts MSE/PE
  connections.  If the tracker supports this parameter, then this peer will not
  be returned in responses to peers that do not set ``supportcrypto=1`` or
  ``requirecrypto=1``.

- ``cryptoport=X`` (used in combination with ``port=0`` and
  ``requirecrypto=1``) — If the tracker supports the ``cryptoport`` parameter,
  it will provide this peer's port as ``X`` in responses to other peers that
  also support MSE/PE and will not provide this peer at all to peers that do
  not support MSE/PE.  If the tracker does not support the ``cryptoport``
  parameter, then this peer's actual port will not be given out to any peers.

When ``supportcrypto=1`` or ``requirecrypto=1`` is set in an announcement to a
supporting HTTP tracker, the response will include a ``crypto_flags`` field,
the value of which is a sequence of bytes, one for each peer in ``peers`` in
order; a given byte will be ``1`` if the peer requires MSE/PE and ``0``
otherwise.

- Preliminary searching on GitHub indicates that, when an HTTP tracker sends a
  response with "``peers``", "``peers6``", and "``crypto_flags``" fields, the
  "``crypto_flags``" only applies to the "``peers``" field and not
  "``peers6``", though I have yet to encounter a tracker that actually sends
  "``crypto_flags``" in the wild.

If a peer prefers MSE/PE connections to unencrypted, it can indicate this to
connecting peers by including an ``e`` field with a value of ``1`` in the `BEP
10`_ extended handshakes it sends.  This ``e`` value will then be broadcast to
other peers using Peer Exchange (`BEP 11`_).


References
==========

- <https://wiki.vuze.com/w/Message_Stream_Encryption> [`Internet Archive Mirror`__]
- <https://css.csail.mit.edu/6.858/2018/projects/bgu-kelvinlu.pdf>
- <https://atomashpolskiy.github.io/bt/encryption/>

__ http://web.archive.org/web/20230405235517/https://wiki.vuze.com/w/Message_Stream_Encryption

.. _BEP 10: https://www.bittorrent.org/beps/bep_0010.html
.. _BEP 11: https://www.bittorrent.org/beps/bep_0011.html
