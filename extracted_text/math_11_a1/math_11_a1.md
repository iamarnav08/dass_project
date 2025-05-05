# **INFINITE SERIES**

# **A.1.1 Introduction**

As discussed in the Chapter 9 on Sequences and Series, a sequence *a*1 , *a*2 , ..., *an* , ... having infinite number of terms is called *infinite sequence* and its indicated sum, i.e., *a*1 + *a*2 + *a*3 + ... + *an* + ... is called an *infinte series* associated with infinite sequence. This series can also be expressed in abbreviated form using the sigma notation, i.e.,

$a_{1}+a_{2}+a_{3}+\cdot\cdot\cdot+a_{n}+\cdot\cdot\cdot=\sum a_{k}$

In this Chapter, we shall study about some special types of series which may be required in different problem situations.

## **A.1.2 Binomial Theorem for any Index**

In Chapter 8, we discussed the Binomial Theorem in which the index was a positive integer. In this Section, we state a more general form of the theorem in which the index is not necessarily a whole number. It gives us a particular type of infinite series, called *Binomial Series*. We illustrate few applications, by examples.

We know the formula

(1 + *x*) *n* = C0 *n* + C1 *n x* + . . . + C *n n x n*

Here, *n* is non-negative integer. Observe that if we replace index *n* by negative

integer or a fraction, then the combinations C *n r* do not make any sense.

We now state (without proof), the Binomial Theorem, giving an infinite series in which the index is negative or a fraction and not a whole number.

**Theorem** The formula

$$\left(1+x\right)^{m}=1+mx+\frac{m\left(m-1\right)}{1.2}x^{2}+\frac{m\left(m-1\right)\left(m-2\right)}{1.2.3}x^{3}+...$$

holds whenever *x* <1.

*Remark* 1. Note carefully the condition | *x* | < 1, i.e., – 1< *x* < 1 is necessary when *m* is negative integer or a fraction. For example, if we take *x* = – 2 and *m* = – 2, we obtain

$$\left(1-2\right)^{-2}=1+\left(-2\right)\left(-2\right)+{\frac{\left(-2\right)\left(-3\right)}{1.2}}\left(-2\right)^{2}+\ldots$$

or 1= 1 + 4 + 12 + . . .

This is not possible

2. Note that there are infinite number of terms in the expansion of (1+ *x*) *m* , when *m* is a negative integer or a fraction

Consider  
  

$$\left(a+b\right)^{m}=\left[a\left(1+\frac{b}{a}\right)\right]^{m}=a^{m}\left(1+\frac{b}{a}\right)^{m}$$
 
$$=a^{m}\left[1+m\frac{b}{a}+\frac{m\left(m-1\right)}{1.2}\left(\frac{b}{a}\right)^{2}+\ldots\right]$$
 
$$=a^{m}+ma^{m-1}b+\frac{m\left(m-1\right)}{1.2}a^{m-2}b^{2}+\ldots$$

This expansion is valid when <1 *b a* or equivalently when | *b* | < | *a* |.

The general term in the expansion of (*a* + *b*) *m* is

$m(m-1)(m-2)...(m-r+1)a^{m-r}b^{r}$  
  
$1.2.3...r$

We give below certain particular cases of Binomial Theorem, when we assume *x* <1, these are left to students as exercises:

1. (1 + *x*) – 1 = 1 – *x* + *x* 2 – *x* 3 + . . . 2. (1 – *x*) – 1 = 1 + *x* + *x* 2 + *x* 3 + . . . 3. (1 + *x*) – 2 = 1 –2 *x* + 3*x* 2 – 4*x* 3 + . . . 4. (1 – *x*) – 2 = 1 +2*x* + 3*x* 2 + 4*x* 3 + . . . **Example 1** Expand 1 2 1 2 *x* − − , when | *x* | < 2.

**Solution** We have

$$\left(1-\frac{x}{2}\right)^{\frac{1}{2}}=1+\frac{\left(-\frac{1}{2}\right)}{1}\left(\frac{-x}{2}\right)+\frac{\left(-\frac{1}{2}\right)\left(-\frac{3}{2}\right)}{1.2}\left(-\frac{x}{2}\right)^{2}+...$$
 
$$=1+\frac{x}{4}+\frac{3x^{2}}{32}+...$$

### **A.1.3 Infinite Geometric Series**

From Chapter 9, Section 9.5, a sequence *a*1 , *a*2 , *a*3 , ..., *an* is called G.P., if *k* +1 *k a a* = *r* (constant) for *k* = 1, 2, 3, ..., *n*–1. Particularly, if we take *a*1 = *a*, then the resulting sequence *a*, *ar*, *ar*2 , ..., *arn*–1 is taken as the standard form of G.P., where *a* is first term and *r*, the common ratio of G.P.

Earlier, we have discussed the formula to find the sum of finite series *a* + *ar* + *ar*2 + ... + *arn* – 1 which is given by

$$S_{n}=\frac{a\left(1-r^{n}\right)}{1-r}\,.$$

In this section, we state the formula to find the sum of infinite geometric series *a* + *ar* + *ar*2 + ... + *arn* – 1 + ... and illustrate the same by examples.

Let us consider the G.P. 1, 2, 4, 9, "

Here $a=1$, $r=2$. We have 

$$S_{n}=\frac{1-\left(\frac{2}{3}\right)^{n}}{1-\frac{2}{3}}=3\left[1-\left(\frac{2}{3}\right)^{n}\right]\tag{1}$$

Let us study the behaviour of 2 3 *n* as *n* becomes larger and larger.

| n |  | 1 | 5 | 10 | 20 |
| --- | --- | --- | --- | --- | --- |
| n  2   |  | 0.6667 | 0.1316872428 | 0.01734152992 | 0.00030072866 |
|   3 |  |  |  |  |  |

We observe that as *n* becomes larger and larger, 2 3 *n* becomes closer and closer to

zero. Mathematically, we say that as *n* becomes sufficiently large, 2 3 *n* becomes

sufficiently small. In other words, as 2 , 0 3 *n n* → ∞ → . Consequently, we find that the sum of infinitely many terms is given by S = 3.

Thus, for infinite geometric progression *a*, *ar*, *ar*2 , ..., if numerical value of common ratio *r* is less than 1, then

$\left(\begin{array}{c}\includegraphics[height=36.135pt]{fig1.eps}\end{array}\right)$

In this case, 0 *n r* → as *n* → ∞ since | | 1 *r* < and then 0 1 *n ar r* → − . Therefore,

* [10] M. C. Gonzalez-Garcia, M. C. Gonzalez-Garcia, M.  
  

Symbolically, sum to infinity of infinite geometric series is denoted by S. Thus,

we have S 1 =

*a r*

−

For example

(i) $1+\frac{1}{2}+\frac{1}{2^{2}}+\frac{1}{2^{3}}+...=\frac{1}{1-\frac{1}{2}}=2$  
  
(ii) $1-\frac{1}{2}+\frac{1}{2^{2}}-\frac{1}{2^{3}}+...=\frac{1}{1-\left(-\frac{1}{2}\right)}=\frac{1}{1+\frac{1}{2}}=\frac{2}{3}$

**Example 2** Find the sum to infinity of the G.P. ;

$$\frac{-5}{4},\frac{5}{16},\frac{-5}{64},....$$
  
  
**Solution** Here $a=\frac{-5}{4}$ and $r=-\frac{1}{4}$. Also $|\,r|<1$.  
  

$$\frac{-5}{4}=\frac{-5}{4}=-1$$
  
  
Hence, the sum to infinity is $\frac{-5}{4}=\frac{-5}{4}=-1$.  
  

## **A.1.4 Exponential Series**

Leonhard Euler (1707 – 1783), the great Swiss mathematician introduced the number *e* in his calculus text in 1748. The number *e* is useful in calculus as π in the study of the circle.

4 4

+

Consider the following infinite series of numbers

1 1 1 1 1 ... 1! 2! 3! 4! + + + + + ... (1)

.

The sum of the series given in (1) is denoted by the number *e*

Let us estimate the value of the number *e*.

Since every term of the series (1) is positive, it is clear that its sum is also positive. Consider the two sums

1 1 1 1 ... ... 3! 4! 5! ! *n* + + + + + ... (2)

and  
  

$$\frac{1}{2^{2}}+\frac{1}{2^{3}}+\frac{1}{2^{4}}+...+\frac{1}{2^{n-1}}+...\tag{3}$$

Observe that

$\frac{1}{2^{2}}=\frac{1}{4}$, which gives $\frac{1}{3!}<\frac{1}{2^{2}}$  
  
$\frac{1}{4!}=\frac{1}{24}$ and $\frac{1}{2^{3}}=\frac{1}{8}$, which gives $\frac{1}{4!}<\frac{1}{2^{3}}$  
  
$\frac{1}{5!}=\frac{1}{120}$ and $\frac{1}{2^{4}}=\frac{1}{16}$, which gives $\frac{1}{5!}<\frac{1}{2^{4}}$

Therefore, by analogy, we can say that

$${\frac{1}{n!}}<{\frac{1}{2^{n-1}}}\,,\,{\mathrm{when}}\,\,n>2$$

We observe that each term in (2) is less than the corresponding term in (3),

Therefore 2 3 4 1 1 1 1 1 1 1 1 1 ... ... ... 3! 4! 5! ! 2 2 2 2*n n* − + + + + < + + + + + ... (4) Adding 1 1 1 1! 2! + + on both sides of (4), we get, 1 1 1 1 1 1 1 ... ... 1! 2! 3! 4! 5! ! *n* + + + + + + + + 2 3 4 1 1 1 1 1 1 1 1 ... ... 1! 2! 2 2 2 2*n*− < + + + + + + + + ... (5) = 2 3 4 1 1 1 1 1 1 1 1 ... ... 2 2 2 2 2*n*− + + + + + + + + = 1 1 1 2 1 1 2 + = + − = 3

Left hand side of (5) represents the series (1). Therefore *e* < 3 and also *e* > 2 and hence 2 < *e* < 3.

*Remark* The exponential series involving variable *x* can be expressed as

$$e^{x}=1+{\frac{x}{1!}}+{\frac{x^{2}}{2!}}+{\frac{x^{3}}{3!}}+\ldots+{\frac{x^{n}}{n!}}+\ldots$$

**Example 3** Find the coefficient of *x* 2 in the expansion of *e* 2*x*+3 as a series in powers of *x*.

**Solution** In the exponential series

$$\stackrel{\mathrm{\scriptsize{~\bar{~}}}}{e^{x}}\,=\,1+\frac{x}{1!}+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\ldots$$

replacing *x* by (2*x* + 3), we get

$$e^{2x+3}=1+{\frac{\left(2x+3\right)}{1!}}+{\frac{\left(2x+3\right)^{2}}{2!}}+\cdots$$

Here, the general term is (2 3) ! *n x n* + = (3+2 ) ! *n x n* . This can be expanded by the

Binomial Theorem as

$${\frac{1}{n!}}\bigg[3^{n}+^{n}\,{\bf C}_{1}3^{n-1}\,\big(2x\big)+^{n}\,{\bf C}_{2}3^{n-2}\,\big(2x\big)^{2}+...+\big(2x\big)^{n}\bigg].$$

Here, the coefficient of *x* 2 is 2 2 C 3 2 2 ! *n n*− *n* . Therefore, the coefficient of *x* 2 in the whole

series is

$$\sum_{n=2}^{\infty}\frac{n\,{\rm C}_{2}\,3^{n-2}2^{2}}{n!}=2\sum_{n=2}^{\infty}\frac{n\,(n-1)3^{n-2}}{n!}$$
 
$$=2\sum_{n=2}^{\infty}\frac{3^{n-2}}{(n-2)!}\,\,\,\,[\mbox{using}n!=n\,(n-1)\,(n\,-\,2)!]$$
 
$$=2\left[1+\frac{3}{1!}+\frac{3^{2}}{2!}+\frac{3^{3}}{3!}+\ldots\right]$$
 
$$=2e^{3}$$

Thus 2*e* 3 is the coefficient of *x* 2 in the expansion of *e* 2*x*+3 . Alternatively *e* 2*x*+3 = *e* 3 . *e* 2*x*

$$=e^{3}\Bigg{[}1+\frac{2x}{1!}+\frac{\left(2x\right)^{2}}{2!}+\frac{\left(2x\right)^{3}}{3!}+...\Bigg{]}$$
  
  
Thus, the coefficient of $x^{2}$ in the expansion of $e^{2x+3}$ is $e^{3}.\frac{2^{2}}{2!}=2e^{3}$

**Example 4** Find the value of *e* 2 , rounded off to one decimal place.

**Solution** Using the formula of exponential series involving *x,* we have

$$e^{x}=1+{\frac{x}{1!}}+{\frac{x^{2}}{2!}}+{\frac{x^{3}}{3!}}+...+{\frac{x^{n}}{n!}}+...$$

Putting *x* = 2, we get

$$e^{2}=1+{\frac{2}{1!}}+{\frac{2^{2}}{2!}}+{\frac{2^{3}}{3!}}+{\frac{2^{4}}{4!}}+{\frac{2^{5}}{5!}}+{\frac{2^{6}}{6!}}+\cdots$$
  
  

$$=1+2+2+{\frac{4}{3}}+{\frac{2}{3}}+{\frac{4}{15}}+{\frac{4}{45}}+\cdots$$

≥ the sum of first seven terms ≥ 7.355.

On the other hand, we have

$$e^{2}<\!\!\left(1+\frac{2}{1!}+\frac{2^{2}}{2!}+\frac{2^{3}}{3!}+\frac{2^{4}}{4!}\right)+\frac{2^{5}}{5!}\!\left(1+\frac{2}{6}+\frac{2^{2}}{6^{2}}+\frac{2^{3}}{6^{3}}+...\right)$$
  
  

$$=7+\frac{4}{15}\!\left(1+\frac{1}{3}+\left(\frac{1}{3}\right)^{2}+...\right)=7+\frac{4}{15}\!\left(\frac{1}{1-\frac{1}{3}}\right)=7+\frac{2}{5}=7.4\,.$$

Thus, *e* 2 lies between 7.355 and 7.4. Therefore, the value of *e* 2 , rounded off to one decimal place, is 7.4.

## **A.1.5 Logarithmic Series**

Another very important series is logarithmic series which is also in the form of infinite series. We state the following result without proof and illustrate its application with an example.

**Theorem** If | *x* | < 1, then

$$\log_{e}\left(1+x\right)=x-{\frac{x^{2}}{2}}+{\frac{x^{3}}{3}}-\cdots$$

The series on the right hand side of the above is called the *logarithmic series*.

A**Note** The expansion of log*e* (1+*x*) is valid for *x* = 1. Substituting *x* = 1 in the expansion of log*e* (1+*x*), we get

$$\log_{e}2=1-{\frac{1}{2}}+{\frac{1}{3}}-{\frac{1}{4}}+\cdots$$

**Example 5** If α β, are the roots of the equation 2 *x px q* − + = 0 , prove that

$$\log_{e}\left(1+px+qx^{2}\right)=\left(\alpha+\beta\right)x-\frac{\alpha^{2}+\beta^{2}}{2}x^{2}+\frac{\alpha^{3}+\beta^{3}}{3}x^{3}-...$$
  
  
**Solution**: Right hand side 
$$=\left[\alpha x-\frac{\alpha^{2}x^{2}}{2}+\frac{\alpha^{3}x^{3}}{3}-...\right]+\left[\beta x-\frac{\beta^{2}x^{2}}{2}+\frac{\beta^{3}x^{3}}{3}-...\right]$$
 
$$=\log_{e}\left(1+\alpha x\right)+\log\left(1+\beta x\right)$$
 
$$=\log_{e}\left(1+\left(\alpha+\beta\right)x+\alpha\beta x^{2}\right)$$
 
$$=\log_{e}\left(1+px+qx^{2}\right)\underset{\text{Left hand side.}}{\text{Left hand side.}}$$

Here, we have used the facts α + β = *p* and αβ = *q* . We know this from the given roots of the quadratic equation. We have also assumed that both | | α *x* < 1 and | | β *x* < 1.

$\begin{array}{c}\includegraphics[height=56.905512pt]{Fig1}\end{array}$

