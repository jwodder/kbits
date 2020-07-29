---
title: Deriving the formula for the sum of $m$-th powers
tags:
    - mathematics
---

The closed-form expression for $\sum_{i=1}^n i^m$ for a given
$m\in\mathbb{Z}^+$ can be derived — once we know the formulas for all lesser
$m$'s — as follows:

- First, observe that:

    \begin{align}
    n^{m+1} & = n^{m+1} - (n-1)^{m+1} \\\\ 
            & + (n-1)^{m+1} - (n-2)^{m+1} \\\\ 
            & + (n-2)^{m+1} - (n-3)^{m+1} \\\\ 
            & + \cdots \\\\ 
            & + 2^{m+1} - 1^{m+1} \\\\ 
            & + 1^{m+1} - 0^{m+1} \\\\ 
            & = \sum_{i=1}^n (i^{m+1} - (i-1)^{m+1})
    \end{align}

- Expand $i^{m+1} - (i-1)^{m+1}$ for the $m$ in question and use the linear
  transformation nature of summation to rewrite the right-hand side of $n^{m+1}
  = \sum_{i=1}^n (i^{m+1} - (i-1)^{m+1})$ as a sum of summations of $i^k$'s.

- Isolate the $\sum_{i=1}^n i^m$ term of the equation.

- Substitute the closed-form expressions for the remaining $\sum_{i=1}^n i^k$
  terms.

For example, once we know that $\sum_{i=1}^n i = \frac{n^2+n}{2}$ and
$\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$, we can derive $\sum_{i=1}^n i^3$
as follows:

\begin{align}
n^4 & = \sum_{i=1}^n (i^4 - (i-1)^4) \\\\ 
    & = \sum_{i=1}^n (4i^3 - 6i^2 + 4i - 1) \\\\ 
    & = 4\sum_{i=1}^n i^3 - 6\sum_{i=1}^n i^2 + 4\sum_{i=1}^n i - n \\\\ 
\sum_{i=1}^n i^3
    & = \frac{1}{4} (n^4 + 6\sum_{i=1}^n i^2 - 4\sum_{i=1}^n i + n) \\\\ 
    & = \frac{1}{4} (n^4 + 6\frac{n(n+1)(2n+1)}{6} - 4\frac{n(n+1)}{2} + n)\\\\ 
    & = \frac{1}{4} (n^4 + 2n^3 + n^2)
\end{align}
