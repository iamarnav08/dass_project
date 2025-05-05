![](_page_0_Picture_0.jpeg)

![](_page_0_Picture_1.jpeg)

# v*The essence of Mathematics lies in its freedom. — CANTOR* v

# **3.1 Introduction**

34 MATHEMATICS

The knowledge of matrices is necessary in various branches of mathematics. Matrices are one of the most powerful tools in mathematics. This mathematical tool simplifies our work to a great extent when compared with other straight forward methods. The evolution of concept of matrices is the result of an attempt to obtain compact and simple methods of solving system of linear equations. Matrices are not only used as a representation of the coefficients in system of linear equations, but utility of matrices far exceeds that use. Matrix notation and operations are used in electronic spreadsheet programs for personal computer, which in turn is used in different areas of business and science like budgeting, sales projection, cost estimation, analysing the results of an experiment etc. Also, many physical operations such as magnification, rotation and reflection through a plane can be represented mathematically by matrices. Matrices are also used in cryptography. This mathematical tool is not only used in certain branches of sciences, but also in genetics, economics, sociology, modern psychology and industrial management.

In this chapter, we shall find it interesting to become acquainted with the fundamentals of matrix and matrix algebra.

# **3.2 Matrix**

Suppose we wish to express the information that Radha has 15 notebooks. We may express it as [15] with the understanding that the number inside [ ] is the number of notebooks that Radha has. Now, if we have to express that Radha has 15 notebooks and 6 pens. We may express it as [15 6] with the understanding that first number inside [ ] is the number of notebooks while the other one is the number of pens possessed by Radha. Let us now suppose that we wish to express the information of possession of notebooks and pens by Radha and her two friends Fauzia and Simran which is as follows:

| Radha | has | 15 | notebooks | and | 6 pens, |
| --- | --- | --- | --- | --- | --- |
| Fauzia | has | 10 | notebooks | and | 2 pens, |
| Simran | has | 13 | notebooks | and | 5 pens. |
|  |  | Now this could be arranged in the tabular form as follows: |  |  |  |

|  | Notebooks | Pens |
| --- | --- | --- |
| Radha | 15 | 6 |
| Fauzia | 10 | 2 |
| Simran | 13 | 5 |

and this can be expressed as

![](_page_1_Figure_5.jpeg)

In the first arrangement the entries in the first column represent the number of note books possessed by Radha, Fauzia and Simran, respectively and the entries in the second column represent the number of pens possessed by Radha, Fauzia and Simran,

respectively. Similarly, in the second arrangement, the entries in the first row represent the number of notebooks possessed by Radha, Fauzia and Simran, respectively. The entries in the second row represent the number of pens possessed by Radha, Fauzia and Simran, respectively. An arrangement or display of the above kind is called a *matrix*. Formally, we define matrix as:

**Definition 1** A *matrix* is an ordered rectangular array of numbers or functions. The numbers or functions are called the elements or the entries of the matrix.

We denote matrices by capital letters. The following are some examples of matrices:

$$\mathbf{A}=\begin{bmatrix}-2&5\\ 0&\sqrt{5}\\ 3&6\end{bmatrix},\ \mathbf{B}=\begin{bmatrix}2+i&3&-\dfrac{1}{2}\\ 3.5&-1&2\\ \sqrt{3}&5&\dfrac{5}{7}\end{bmatrix},\ \mathbf{C}=\begin{bmatrix}1+x&x^{3}&3\\ \cos x&\sin x+2&\tan x\end{bmatrix}$$

In the above examples, the horizontal lines of elements are said to constitute, *rows* of the matrix and the vertical lines of elements are said to constitute, *columns* of the matrix. Thus A has 3 rows and 2 columns, B has 3 rows and 3 columns while C has 2 rows and 3 columns.

#### **3.2.1** *Order of a matrix*

A matrix having *m* rows and *n* columns is called a matrix of *order m* × *n* or simply *m* × *n* matrix (read as an *m* by *n* matrix). So referring to the above examples of matrices, we have A as 3 × 2 matrix, B as 3 × 3 matrix and C as 2 × 3 matrix. We observe that A has 3 × 2 = 6 elements, B and C have 9 and 6 elements, respectively.

In general, an *m* × *n* matrix has the following rectangular array:

| a11 | a 12 | a13 ... a; ··· aln |
| --- | --- | --- |
| ası a lå | a22 م •••• م••• | do ... day ... all ... mx j |

or A = [*aij*] *m* × *n* , 1≤ *i* ≤ *m*, 1≤ *j* ≤ *n i*, *j* ∈ N

Thus the *i* th row consists of the elements *ai*1 , *ai*2 , *ai*3 ,..., *ain*, while the *j* th column consists of the elements *a*1*j* , *a*2*j* , *a*3*j* ,..., *amj* ,

In general *aij*, is an element lying in the *i* th row and *j* th column. We can also call it as the (*i*, *j*) th element of A. The number of elements in an *m* × *n* matrix will be equal to *mn*.

A**Note** In this chapter

- 1. We shall follow the notation, namely A = [*aij*] *m* × *n* to indicate that A is a matrix of order *m* × *n*.
- 2. We shall consider only those matrices whose elements are real numbers or functions taking real values.

We can also represent any point (*x*, *y*) in a plane by a matrix (column or row) as *x y* (or [*x*, *y*]). For example point P(0, 1) as a matrix representation may be given as

$$\mathbf{P}={\begin{bmatrix}0\\ 1\end{bmatrix}}{\mathrm{~or~}}[0\ 1].$$

Observe that in this way we can also express the vertices of a closed rectilinear figure in the form of a matrix. For example, consider a quadrilateral ABCD with vertices A (1, 0), B (3, 2), C (1, 3), D (–1, 2).

Now, quadrilateral ABCD in the matrix form, can be represented as

2 4 A B C D 1 3 1 1 X 0 2 3 2 × − = or 4 2 A 1 0 B 3 2 Y C 1 3 D 1 2 × = −

Thus, matrices can be used as representation of vertices of geometrical figures in a plane.

Now, let us consider some examples.

**Example 1** Consider the following information regarding the number of men and women workers in three factories I, II and III

|  | Men workers | Women workers |
| --- | --- | --- |
| I | 30 | 25 |
| II | 25 | 31 |
| III | 27 | 26 |

Represent the above information in the form of a 3 × 2 matrix. What does the entry in the third row and second column represent?

**Solution** The information is represented in the form of a 3 × 2 matrix as follows:

$$\mathbf{A}={\left[\begin{array}{l l}{30}&{25}\\ {25}&{31}\\ {27}&{26}\end{array}\right]}$$

The entry in the third row and second column represents the number of women workers in factory III.

**Example 2** If a matrix has 8 elements, what are the possible orders it can have?

**Solution** We know that if a matrix is of order *m* × *n*, it has *mn* elements. Thus, to find all possible orders of a matrix with 8 elements, we will find all ordered pairs of natural numbers, whose product is 8.

Thus, all possible ordered pairs are (1, 8), (8, 1), (4, 2), (2, 4)

Hence, possible orders are 1 × 8, 8 ×1, 4 × 2, 2 × 4

**Example 3** Construct a 3 × 2 matrix whose elements are given by 1 | 3 | 2 *ij a i j* = − *.*

  
  
**Solution** In general a $3\times2$ matrix is given by $\mathbf{A}=\begin{bmatrix}a_{11}&a_{12}\\ a_{21}&a_{22}\\ a_{31}&a_{32}\end{bmatrix}$.  
  

Now

$a_{ij}=\frac{1}{2}i-3j1$, $i=1,2,3$ and $j=1,2$.  
  

Therefore 11 1 |1 3 1| 1 2 *a* = − × = 12 1 5 |1 3 2 | 2 2 *a* = − × = 21 1 1 | 2 3 1| 2 2 *a* = − × = 22 1 | 2 3 2 | 2 2 *a* = − × = 31 1 | 3 3 1| 0 2 *a* = − × = 32 1 3 | 3 3 2 | 2 2 *a* = − × = Hence the required matrix is given by 5 1 2 1 A 2 2 3 0 2 = .

#### **3.3 Types of Matrices**

In this section, we shall discuss different types of matrices.

- (i) **Column matrix**
A matrix is said to be a *column matrix* if it has only one column.

For example, $\mathbf{A}=\begin{bmatrix}0\\ \sqrt{3}\\ -1\\ 1/2\end{bmatrix}$ is a column matrix of order $4\times1$.  
  

In general, A = [*aij*] *m* × 1 is a column matrix of order *m* × 1.

#### (ii) **Row matrix**

A matrix is said to be a *row matrix* if it has only one row.

For example, $\mathbf{B=}\left[-\frac{1}{2}\sqrt{5}\ 2\ 3\right]_{1\times4}$ is a row matrix.  
  

In general, B = [*bij*] 1 × *n* is a row matrix of order 1 × *n*.

#### (iii) **Square matrix**

A matrix in which the number of rows are equal to the number of columns, is said to be a *square matrix*. Thus an *m* × *n* matrix is said to be a square matrix if *m* = *n* and is known as a square matrix of order '*n*'.

For example $\mathbf{A}=\begin{bmatrix}3&-1&0\\ 3&3\sqrt{2}&1\\ 4&3&-1\end{bmatrix}$ is a square matrix of order 3.  
  

In general, A = [*aij*] *m* × *m* is a square matrix of order *m*.

A**Note** If A = [*aij*] is a square matrix of order *n*, then elements (entries) *a*11, *a*22*, ...*, *ann* are said to constitute the *diagonal*, of the matrix A. Thus, if 1 3 1 A 2 4 1 3 5 6 − = − . Then the elements of the diagonal of A are 1, 4, 6.

#### (iv) **Diagonal matrix**

A square matrix B = [*bij*] *m* × *m* is said to be a *diagonal matrix* if all its non diagonal elements are zero, that is a matrix B = [*bij*] *m* × *m* is said to be a diagonal matrix if *bij* = 0, when *i* ≠ *j*.

For example, A = [4], 1 0 B 0 2 − = , 1.1 0 0 C 0 2 0 0 0 3 − = , are diagonal matrices

of order 1, 2, 3, respectively.

#### (v) **Scalar matrix**

A diagonal matrix is said to be a *scalar matrix* if its diagonal elements are equal, that is, a square matrix B = [*bij*] *n* × *n* is said to be a scalar matrix if

$b_{ij}=0$, when $i\neq j$  
  
$b_{ij}=k$, when $i=j$, for some constant $k$.  
  

For example

$\mathbf{A}=[3]$, $\mathbf{B}=\begin{bmatrix}-1&0\\ 0&-1\end{bmatrix}$, $\mathbf{C}=\begin{bmatrix}0&0\\ 0&\sqrt{3}&0\\ 0&0&\sqrt{3}\end{bmatrix}$.  
  

are scalar matrices of order 1, 2 and 3, respectively.

#### (vi) **Identity matrix**

A square matrix in which elements in the diagonal are all 1 and rest are all zero is called an *identity matrix*. In other words, the square matrix A = [*aij*] *n* × *n* is an

identity matrix, if 1 if 0 if *ij i j a i j* = = ≠ .

We denote the identity matrix of order *n* by I *n .* When order is clear from the context, we simply write it as I.

For example [1], $\begin{bmatrix}1&0\\ 0&1\end{bmatrix}$, $\begin{bmatrix}1&0&0\\ 0&1&0\\ 0&0&1\end{bmatrix}$ are identity matrices of order 1, 2 and 3,

respectively.

Observe that a scalar matrix is an identity matrix when *k* = 1. But every identity matrix is clearly a scalar matrix.

#### (vii) **Zero matrix**

A matrix is said to be *zero matrix* or *null matrix* if all its elements are zero.

For example, [0], 0 0 0 0 , 0 0 0 0 0 0 , [0, 0] are all zero matrices. We denote zero matrix by O. Its order will be clear from the context.

#### **3.3.1** *Equality of matrices*

**Definition 2** Two matrices A = [*aij*] and B = [*bij*] are said to be equal if

- (i) they are of the same order
- (ii) each element of A is equal to the corresponding element of B, that is *aij* = *bij* for all *i* and *j*.

For example, 2 3 2 3 and 0 1 0 1 are equal matrices but 3 2 2 3 and 0 1 0 1 are

not equal matrices. Symbolically, if two matrices A and B are equal, we write A = B.

$$\text{If}\begin{bmatrix}x&y\\ z&a\\ b&c\end{bmatrix}=\begin{bmatrix}-1.5&0\\ 2&\sqrt{6}\\ 3&2\end{bmatrix},\text{then}x=\begin{bmatrix}1.5,y=0,z=2\\ 0,z=2\end{bmatrix},a=\sqrt{6},b=3,c=2.$$
  
  
**Example 4**: $\text{If}\begin{bmatrix}x+3&2+4&2y-7\\ -6&a^{\prime}-1&0\\ b-3&-21&0\end{bmatrix}=\begin{bmatrix}0&6&3y-2\\ -6&-3&2c+2\\ 2b+4&-21&0\end{bmatrix}$

Find the values of *a*, *b*, *c*, *x*, *y* and *z*.

**Solution** As the given matrices are equal, therefore, their corresponding elements must be equal. Comparing the corresponding elements, we get

$x+3=0$, $z+4=6$, $2y-7=3y-2$  
  
$a=1=-3$, $0=2c+2$ $b-3=2b+4$,

Simplifying, we get

$$a=-\ 2,\,b=-\ 7,\,c=-\ 1,\,x=-\ 3,\,y=-5,\,z=2$$

**Example 5** Find the values of *a*, *b*, *c*, and *d* from the following equation:

$${\left[\begin{array}{l l}{2a+b}&{a-2b}\\ {5c-d}&{4c+3d}\end{array}\right]}={\left[\begin{array}{l l}{4}&{-3}\\ {11}&{24}\end{array}\right]}$$

**Solution** By equality of two matrices, equating the corresponding elements, we get

$$\begin{array}{l l}{{2a+b=4}}&{{\qquad\qquad5c-d=11}}\\ {{a-2b=-3}}&{{\qquad4c+3d=24}}\end{array}$$

Solving these equations, we get

$$a=1,\,b=2,\,c=3{\mathrm{~and~}}d=4$$

**EXERCISE 3.1**

- **1.** In the matrix 2 5 19 7 5 A 35 2 12 2 3 1 5 17 − = − − , write:
	- (i) The order of the matrix, (ii) The number of elements,
	- (iii) Write the elements *a*13, *a*21, *a*33, *a*24, *a*23.
- **2.** If a matrix has 24 elements, what are the possible orders it can have? What, if it has 13 elements?
- **3.** If a matrix has 18 elements, what are the possible orders it can have? What, if it has 5 elements?
- **4.** Construct a 2 × 2 matrix, A = [*aij*], whose elements are given by:

(i) $a_{ij}=\frac{\left(i+j\right)^{2}}{2}$ (ii) $a_{ij}=\frac{\left(i+2j\right)^{2}}{2}$

- **5.** Construct a 3 × 4 matrix, whose elements are given by:
(i) $a_{ij}=\frac{1}{2}|-3i+j|$ (ii) $a_{ij}=2i-j$

- **6.** Find the values of *x*, *y* and *z* from the following equations:
(i) 4 3 5 1 5 *y z x* = (ii) 2 6 2 5 5 8 *x y z xy* + = + (iii) 9 5 7 *x y z x z y z* + + + = +

- **7.** Find the value of *a*, *b*, *c* and *d* from the equation:

$${\left[\begin{array}{l l}{a-b}&{2a+c}\\ {2a-b}&{3c+d}\end{array}\right]}={\left[\begin{array}{l l}{-1}&{5}\\ {0}&{13}\end{array}\right]}$$

- **8.** A = [*aij*] *m* × *n\* is a square matrix, if (A) *m* < *n* (B) *m* > *n* (C) *m* = *n* (D) None of these **9.** Which of the given values of *x* and *y* make the following pair of matrices equal 3 7 5 1 2 3 *x y x* + + − , 0 2 8 4 *y* − (A) 1 , 7 3 *x y* − = = (B) Not possible to find (C) *y* = 7, 2 3 *x* − = (D) 1 2 , 3 3 *x y* − − = =
- **10.** The number of all possible matrices of order 3 × 3 with each entry 0 or 1 is: (A) 27 (B) 18 (C) 81 (D) 512

# **3.4 Operations on Matrices**

In this section, we shall introduce certain operations on matrices, namely, addition of matrices, multiplication of a matrix by a scalar, difference and multiplication of matrices.

### **3.4.1** *Addition of matrices*

Suppose Fatima has two factories at places A and B. Each factory produces sport shoes for boys and girls in three different price categories labelled 1, 2 and 3. The quantities produced by each factory are represented as matrices given below:

|  | Factory at A |  |  |  | Factory at B |
| --- | --- | --- | --- | --- | --- |
|  | Boys | Girls |  | Boys | Girls |
|  | 80 | 60 |  | 90 | 50 |
| ನ | 75 | 65 | 2 | 70 | રેરે |
| ಗ | 90 | 8ર | ನ | 75 | 75 |

Suppose Fatima wants to know the total production of sport shoes in each price category. Then the total production

In category 1 : for boys (80 + 90), for girls (60 + 50)

In category 2 : for boys (75 + 70), for girls (65 + 55)

In category 3 : for boys (90 + 75), for girls (85 + 75)

|  | 80  | + | 90 | 60 | + 50 |  |
| --- | --- | --- | --- | --- | --- | --- |
| This can be represented in the matrix form as |  |  |  |  |  |  . |
|  | 75  | + | 70 | 65 | + 55 |  |
|  |  90  | + | 75 | 85 | + 75 |   |

This new matrix is the **sum** of the above two matrices. We observe that the sum of two matrices is a matrix obtained by adding the corresponding elements of the given matrices. Furthermore, the two matrices have to be of the same order.

Thus, if $\ A=\begin{bmatrix}a_{11}&a_{12}&a_{13}\\ a_{21}&a_{22}&a_{23}\end{bmatrix}$ is a $2\times3$ matrix and $\ B=\begin{bmatrix}b_{11}&b_{12}&b_{13}\\ b_{21}&b_{22}&b_{23}\end{bmatrix}$ is another 

2×3 matrix. Then, we define 11 11 12 12 13 13 21 21 22 22 23 23 A + B *a b a b a b a b a b a b* + + + = + + + .

In general, if A = [*aij*] and B = [*bij*] are two matrices of the same order, say *m* × *n*. Then, the sum of the two matrices A and B is *defined* as a matrix C = [*cij*] *m* × *n* , where *cij* = *aij* + *bij*, for all possible values of *i* and *j*.

  
  
**Example 6**: Given A = $\begin{bmatrix}\sqrt{3}&1&-1\\ 2&3&0\end{bmatrix}$ and B = $\begin{bmatrix}2&\sqrt{5}&1\\ -2&3&\frac{1}{2}\end{bmatrix}$, find A+ B

Since A, B are of the same order 2 × 3. Therefore, addition of A and B is defined and is given by

$$\mathbf{A}+\mathbf{B}=\begin{bmatrix}2+\sqrt{3}&1+\sqrt{5}&1-1\\ 2-2&3+3&0+\frac{1}{2}\end{bmatrix}=\begin{bmatrix}2+\sqrt{3}&1+\sqrt{5}&0\\ 0&6&\frac{1}{2}\end{bmatrix}$$

# A**Note**

- 1. We emphasise that if A and B are not of the same order, then A + B is not
defined. For example if 2 3 A 1 0 = , 1 2 3 B , 1 0 1 = then A + B is not defined.

- 2. We may observe that addition of matrices is an example of binary operation on the set of matrices of the same order.
#### **3.4.2** *Multiplication of a matrix by a scalar*

Now suppose that Fatima has doubled the production at a factory A in all categories (refer to 3.4.1).

Previously quantities (in standard units) produced by factory A were

|  | Boys | Girls |
| --- | --- | --- |
| 1 | 80 | 60 |
| 2 | 75 | ર્ણ |
| 3 | 90 | 8 રે |

Revised quantities produced by factory A are as given below:

|  |  |  | Boys |  |  | Girls |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  | 2 | × | 80 | 2 | × | 60 |  |
| 2 |  |  |  |  |  |  |  |  |
|  |  | 2 | × | 75 | 2 | × | 65 |  |
| 3 |   | 2 | × | 90 | 2 | × | 85 |   |

This can be represented in the matrix form as 160 120 150 130 180 170 . We observe that

the new matrix is obtained by multiplying each element of the previous matrix by 2.

In general, we may define *multiplication of a matrix* by a scalar as follows: if A = [*aij*] *m* × *n* is a matrix and *k* is a scalar, then *k*A is another matrix which is obtained by multiplying each element of A by the scalar *k*.

In other words, *k*A = *k* [*aij*] *m* × *n* = [*k* (*aij*)] *m* × *n* , that is, (*i*, *j*) th element of *k*A is *kaij* for all possible values of *i* and *j*.

| 3 | 1 | 1.5 |  |  |  |  | For example, if | A = | , then |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| − | 5 | 7 | 3 |  |  |  |  | 2 | 0 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | 3 | 1 | 1.5 |  |  | 9 | 3 | 4.5 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| − | = | − | 3A = | 3 | 5 | 7 | 3 | 3 | 5 | 21 | 9 |  |  |  |  |  |  |  |  | 2 | 0 | 5 | 6 | 0 | 15 |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

**Negative of a matrix** The negative of a matrix is denoted by – A. We define –A = (– 1) A.

For example, let  
  

$$\text{A}=\begin{bmatrix}3&1\\ -5&x\end{bmatrix},\text{then}-\text{A}\text{is given by}$$
  
  

$$-\text{A}=(-\ 1)\,\text{A}=(-1)\begin{bmatrix}3&1\\ -5&x\end{bmatrix}=\begin{bmatrix}-3&-1\\ 5&-x\end{bmatrix}$$

**Difference of matrices** If A = [*aij*], B = [*bij*] are two matrices of the same order, say *m* × *n*, then difference A – B is defined as a matrix D = [*dij*], where *dij* = *aij* – *bij*, for all value of *i* and *j*. In other words, D = A – B = A + (–1) B, that is sum of the matrix A and the matrix – B.

  
  
**Example 7** If $\,\mathrm{A}=\begin{bmatrix}1&2&3\\ 2&3&1\end{bmatrix}$ and $\,\mathrm{B}=\begin{bmatrix}3&-1&3\\ -1&0&2\end{bmatrix}$, then find $\,2\mathrm{A}-\mathrm{B}$.  
  

**Solution** We have

$2\,\mathrm{A}-\mathrm{B}=2\left[\begin{array}{cccc}1&2&3\\ 2&3&1\end{array}\right]-\left[\begin{array}{cccc}3&-1&3\\ -1&0&2\end{array}\right]$  
  
$=\left[\begin{array}{cccc}2&4&6\\ 4&6&2\end{array}\right]+\left[\begin{array}{cccc}-3&1&-3\\ 1&0&2\end{array}\right]$  
  
$=\left[\begin{array}{cccc}2&-3&4+1&6-3\\ 4+1&6+0&2-2\end{array}\right]=\left[\begin{array}{cccc}-1&5&3\\ 5&6&0\end{array}\right]$

#### **3.4.3** *Properties of matrix addition*

The addition of matrices satisfy the following properties:

- (i) **Commutative Law** If A = [*aij*], B = [*bij*] are matrices of the same order, say *m* × *n*, then A + B = B + A.
	- Now A + B = [*aij*] + [*bij*] = [*aij* + *bij*] = [*bij* + *aij*] (addition of numbers is commutative) = ([*bij*] + [*aij*]) = B + A
- (ii) **Associative Law** For any three matrices A = [*aij*], B = [*bij*], C = [*cij*] of the same order, say *m* × *n*, (A + B) + C = A + (B + C).

Now (A + B) + C = ([$a_{\,\,\,\,j}$] + [$b_{\,\,\,\,j}$]) + [$c_{\,\,\,\,j}$] 
$$=[a_{\,\,\,\,j}\,+\,b_{\,\,\,\,j}]\,+\,[c_{\,\,\,\,j}]=[(a_{\,\,\,\,j}\,+\,b_{\,\,\,\,j})\,+\,c_{\,\,\,\,j}]$$
 
$$=[a_{\,\,\,\,j}\,+\,(b_{\,\,\,\,j}\,+\,c_{\,\,\,\,j})]$$
 (Why?) 
$$=[a_{\,\,\,\,j}]\,+\,[(b_{\,\,\,\,j}\,+\,c_{\,\,\,\,j})]=[a_{\,\,\,\,j}]\,+\,[(b_{\,\,\,\,j}]\,+\,[c_{\,\,\,\,j}]]=\mbox{A+(B+C)}$$

- (iii) **Existence of additive identity** Let A = [*aij*] be an *m* × *n* matrix and O be an *m* × *n* zero matrix, then A + O = O + A = A. In other words, O is the additive identity for matrix addition.
- (iv) **The existence of additive inverse** Let A = [*aij*] *m* × *n* be any matrix, then we have another matrix as – A = [– *aij*] *m* × *n* such that A + (– A) = (– A) + A= O. So – A is the additive inverse of A or negative of A.

#### **3.4.4** *Properties of scalar multiplication of a matrix*

If A = [*aij*] and B = [*bij*] be two matrices of the same order, say *m* × *n*, and *k* and *l* are scalars, then

- (i) *k*(A +B) = *k* A + *k*B, (ii) (*k* + *l*)A = *k* A + *l* A
(ii) $k$ (A + B) = $k$ ([$a_{ij}$] + [$b_{ij}$])  
  

$$=k\ [a_{ij}+b_{ij}]=[k\ (a_{ij}+b_{ij})]=[(k\ a_{ij})+(k\ b_{ij})]$$
 =[k\ a_{ij}]+[k\ b_{ij}]=k\ [a_{ij}]+\hat{k}\ [b_{ij}]=k\)A+kB\)

(iii) $(\,k+l)\,\,\mathrm{A}=(k+l)\,\,[a_{ij}]$  
  

$$=[(k+l)\,\,a_{ij}]+[k\,a_{ij}]+[l\,a_{ij}]=k\,\,[a_{ij}]+[l\,a_{ij}]=k\,\,\mathrm{A}+l\,\,\mathrm{A}$$

**Example 8** If 8 0 2 2 A 4 2 and B 4 2 3 6 5 1 − = − = − , then find the matrix X, such that

2A + 3X = 5B.

#### **Solution** We have 2A + 3X = 5B

or 2A + 3X – 2A = 5B – 2A

1 3

(5B – 2A)

or 2A – 2A + 3X = 5B – 2A (Matrix addition is commutative) or O + 3X = 5B – 2A (– 2A is the additive inverse of 2A) or 3X = 5B – 2A (O is the additive identity)

or X =

or

$$\mathrm{X}=\frac{1}{3}\!\left(\begin{array}{ccc}5&2&-2\\ 4&2\\ -5&1\end{array}\right)\!-2\!\left(\begin{array}{ccc}8&0\\ 4&-2\\ 3&6\end{array}\right)\right)=\frac{1}{3}\!\left(\begin{array}{ccc}10&-10\\ 20&10\\ -25&5\end{array}\right)+\left[\begin{array}{ccc}-16&0\\ -8&4\\ -6&-12\end{array}\right)\right)$$

$$=\frac{1}{3}\left[\begin{array}{ccc}10-16&-10+0\\ 20-8&10+4\\ -25-6&5-12\end{array}\right]=\frac{1}{3}\left[\begin{array}{ccc}-6&-10\\ 12&14\\ -31&-7\end{array}\right]=\left[\begin{array}{ccc}-2&\frac{-10}{3}\\ 4&\frac{14}{3}\\ \frac{-31}{3}&\frac{-7}{3}\end{array}\right]$$

.

  
  
**Example 9** Find X and Y, if X + Y = $\begin{bmatrix}5&2\\ 0&9\end{bmatrix}$ and X - Y = $\begin{bmatrix}3&6\\ 0&-1\end{bmatrix}$.  
  

**Solution** We have ( ) ( ) 5 2 3 6 X Y X Y 0 9 0 1 + + − = + −

or  
  

$$(X+X)+(Y-Y)=\left[\begin{array}{cc}8&8\\ 0&8\end{array}\right]\Rightarrow2X=\left[\begin{array}{cc}8&8\\ 0&8\end{array}\right]$$
  
  
or  
  

$$X=\frac{1}{2}\left[\begin{array}{cc}8&8\\ 0&8\end{array}\right]=\left[\begin{array}{cc}4&4\\ 0&4\end{array}\right]$$

Also (X + Y) – (X – Y) = 5 2 3 6

Also  
  

$$(X+Y)-(X=Y)=\left[\begin{array}{cc}0&0\\ 0&-1\end{array}\right]$$
  
  
or  
  

$$(X-X)+(Y+Y)=\left[\begin{array}{cc}5-3&2-6\\ 0&9+1\end{array}\right]\Rightarrow2Y=\left[\begin{array}{cc}2&-4\\ 0&10\end{array}\right]$$

$$\mathrm{Y}=\frac{1}{2}\begin{bmatrix}2&-4\\ 0&10\end{bmatrix}=\begin{bmatrix}1&-2\\ 0&5\end{bmatrix}$$

**Example 10** Find the values of *x* and *y* from the following equation:

$$2{\left[\begin{matrix}x&5\\ 7&y-3\end{matrix}\right]}+{\left[\begin{matrix}3&-4\\ 1&2\end{matrix}\right]}={\left[\begin{matrix}7&6\\ 15&14\end{matrix}\right]}$$

**Solution** We have

$$2\begin{bmatrix}x&5\\ 7&y-3\end{bmatrix}+\begin{bmatrix}3&-4\\ 1&2\end{bmatrix}=\begin{bmatrix}7&6\\ 15&14\end{bmatrix}\Rightarrow\begin{bmatrix}2x&10\\ 14&2y-6\end{bmatrix}+\begin{bmatrix}3&-4\\ 1&2\end{bmatrix}=\begin{bmatrix}7&6\\ 15&14\end{bmatrix}$$

or 2 3 10 4 14 1 2 6 2 *x y* + − + − + = 7 6 15 14 ⇒ 2 3 6 7 6 15 2 4 15 14 *x y* + = − or 2*x* + 3 = 7 and 2*y* – 4 = 14 (Why?) or 2*x* = 7 – 3 and 2*y* = 18 or *x* = 4 2 and *y* = 18 2 i.e. *x* = 2 and *y* = 9.

**Example 11** Two farmers Ramkishan and Gurcharan Singh cultivates only three varieties of rice namely Basmati, Permal and Naura. The sale (in Rupees) of these varieties of rice by both the farmers in the month of September and October are given by the following matrices A and B.

|  |  | September Sales (in Rupees) |  |  |
| --- | --- | --- | --- | --- |
|  | Basmati | Permal | Naura |  |
| A = | 10,000 | 20,000 | 30,000 | Ramkishan |
|  | 50,000 | 30,000 | 10,000 | Gurcharan Singh |

|  | Basmati | Permal | > Naura |  |
| --- | --- | --- | --- | --- |
| B = | 5000 | 10,000 | 6000 | Ramkishan |
|  | 20.000 | 10.000 | 10,000 | Gurcharan Singh |

- (i) Find the combined sales in September and October for each farmer in each variety.
- (ii) Find the decrease in sales from September to October.
- (iii) If both farmers receive 2% profit on gross sales, compute the profit for each farmer and for each variety sold in October.

#### **Solution**

- (i) Combined sales in September and October for each farmer in each variety is given by

|  | Basmati | Permal | Naura |  |
| --- | --- | --- | --- | --- |
| A + B = | 15,000 | 30.000 | 36,000 | Ramkishan |
|  | 70,000 | 40,000 | 20,000 | Gurcharan Singh |

(ii) Change in sales from September to October is given by

$$\begin{array}{ccccc}\text{Basmati}&\text{Permal}&\text{Naura}\\ \text{A}-\text{B}=\left[\begin{array}{ccccc}5000&10,000&24,000\\ 30,000&20,000&0\end{array}\right]\text{Ramkishan}\\ \cdot\\ \text{Bamati}&\text{Permal}&\text{Naura}\\ =&0.02\left[\begin{array}{ccccc}5000&10,000&6000\\ 20,000&10,000&10,000\end{array}\right]\text{Ramkishan}\\ \text{Basmati}&\text{Permal}&\text{Naura}\\ =&\left[\begin{array}{ccccc}100&200&200\\ 400&200&200\end{array}\right]\text{Ramkishan}\\ \end{array}$$

Thus, in October Ramkishan receives ` 100, ` 200 and ` 120 as profit in the sale of each variety of rice, respectively, and Grucharan Singh receives profit of `400, ` 200 and ` 200 in the sale of each variety of rice, respectively.

## **3.4.5** *Multiplication of matrices*

Suppose Meera and Nadeem are two friends. Meera wants to buy 2 pens and 5 story books, while Nadeem needs 8 pens and 10 story books. They both go to a shop to enquire about the rates which are quoted as follows:

Pen – ` 5 each, story book – ` 50 each.

How much money does each need to spend? Clearly, Meera needs ` (5 × 2 + 50 × 5) that is ` 260, while Nadeem needs (8 × 5 + 50 × 10) `, that is ` 540. In terms of matrix representation, we can write the above information as follows:

**Requirements Prices per piece (in Rupees) Money needed (in Rupees)**

|   |  |  |
| --- | --- | --- |
| 8 |  | 2 |
| 10 |  | 5 |
|   |  |  |
|   50   |  |  5  |
|  8  |  |  5 |
| × |  | × |
| 5 |  | 2 |
| + |  | + |
| 10 |  | 5 |
| × 50 |  | × 50 |
|   | = |  |
|  540  |  |  260 |
|   |  |  |

Suppose that they enquire about the rates from another shop, quoted as follows: pen – ` 4 each, story book – ` 40 each.

Now, the money required by Meera and Nadeem to make purchases will be respectively ` (4 × 2 + 40 × 5) = ` 208 and ` (8 × 4 + 10 × 40) = ` 432

Again, the above information can be represented as follows:

**Requirements Prices per piece (in Rupees) Money needed (in Rupees)**

$$\begin{bmatrix}2&5\\ 8&10\end{bmatrix}\qquad\qquad\qquad\qquad\begin{bmatrix}4\\ 40\end{bmatrix}\qquad\qquad\qquad\qquad\begin{bmatrix}4\times2+40\times5\\ 8\times4\ +10\times4\ 0\end{bmatrix}=\begin{bmatrix}208\\ 432\end{bmatrix}$$

Now, the information in both the cases can be combined and expressed in terms of matrices as follows:

**Requirements Prices per piece (in Rupees) Money needed (in Rupees)**

| × | + | × | × | + | × |  | 2 | 5 |  |  | 5 | 4 |  |  | 5 | 2 | 5 | 50 | 4 | 2 | 40 | 5 |  |  |  |  |  |  |  | × | + | × | × | + | × | 8 | 10 | 50 | 40 | 8 | 5 | 10 | 5 0 8 | 4 | 10 | 4 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 260 | 208 |  |  | = |  |  | 540 | 432 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

The above is an example of multiplication of matrices. We observe that, for multiplication of two matrices A and B, the number of columns in A should be equal to the number of rows in B. Furthermore for getting the elements of the product matrix, we take rows of A and columns of B, multiply them element-wise and take the sum. Formally, we define multiplication of matrices as follows:

The *product* of two matrices A and B is *defined* if the number of columns of A is equal to the number of rows of B. Let A = [*aij*] be an *m* × *n* matrix and B = [*bjk*] be an *n* × *p* matrix. Then the product of the matrices A and B is the matrix C of order *m* × *p*. To get the (*i*, *k*) th element *cik* of the matrix C, we take the *i* th row of A and *k* th column of B, multiply them elementwise and take the sum of all these products. In other words, if A = [*aij*] *m* × *n* , B = [*bjk*] *n* × *p* , then the *i* th row of A is [*ai*1 *ai*2 ... *ain*] and the *k* th column of

$$\mathrm{B}\ \mathrm{is}\ \left[\begin{array}{c}b_{1k}\\ b_{2k}\\ \vdots\\ b_{n k}\end{array}\right],\ \mathrm{then}\,\hat{C}_{a k}=\ a_{i_{1}}\,b_{1k}+\,a_{i_{2}}\,b_{2k}+\,a_{i_{3}}\,b_{3k}+\,\ldots\,+\,a_{i_{n}}\,b_{n k}=\sum_{j=1}^{n}a_{i j}\,b_{j k}\ .$$

The matrix C = [*cik*] *m* × *p* is the product of A and B.

For example, if C = $\begin{bmatrix}1&-1&2\\ 0&3&4\end{bmatrix}$ and D = $\begin{bmatrix}2&7\\ -1&1\\ 5&-4\end{bmatrix}$, then the product CD is defined 

and is given by 2 7 1 1 2 CD 1 1 0 3 4 5 4 − = − − . This is a 2 × 2 matrix in which each

entry is the sum of the products across some row of C with the corresponding entries down some column of D. These four computations are

Thus 13 2 CD 17 13 − = − **Example 12** Find AB, if 6 9 2 6 0 A and B 2 3 7 9 8 = = .

**Solution** The matrix A has 2 columns which is equal to the number of rows of B. Hence AB is defined. Now

$$\begin{array}{l}\mbox{AB}=\begin{bmatrix}6(2)+9(7)&6(6)+9(9)&6(0)+9(8)\\ 2(2)+3(7)&2(6)+3(9)&2(0)+3(8)\end{bmatrix}\\ \\ =\begin{bmatrix}12+63&36+81&0+72\\ 4+21&12+27&0+24\end{bmatrix}=\begin{bmatrix}75&117&72\\ 25&39&24\end{bmatrix}\end{array}$$

*Remark* If AB is defined, then BA need not be defined. In the above example, AB is defined but BA is not defined because B has 3 column while A has only 2 (and not 3) rows. If A, B are, respectively *m* × *n*, *k* × *l* matrices, then both AB and BA are defined **if and only if** *n* = *k* and *l* = *m*. In particular, if both A and B are square matrices of the same order, then both AB and BA are defined.

#### **Non-commutativity of multiplication of matrices**

Now, we shall see by an example that even if AB and BA are both defined, it is not necessary that AB = BA.

  
  
**Example 13**: If A = $\begin{bmatrix}1&-2&3\\ -4&2&5\end{bmatrix}$ and B = $\begin{bmatrix}2&3\\ 4&5\\ 2&1\end{bmatrix}$, then find AB, BA. Show that

AB ≠ BA.

**Solution** Since A is a 2 × 3 matrix and B is 3 × 2 matrix. Hence AB and BA are both defined and are matrices of order 2 × 2 and 3 × 3, respectively. Note that

$$\text{AB}=\begin{bmatrix}1&-2&3\\ -4&2&5\end{bmatrix}\begin{bmatrix}2&3\\ 4&5\\ 2&1\end{bmatrix}=\begin{bmatrix}2-8+6&3-10+3\\ -8+8+10&-12+10+5\end{bmatrix}=\begin{bmatrix}0&-4\\ 10&3\end{bmatrix}$$
  
  

$$\text{BA}=\begin{bmatrix}2&3\\ 4&5\\ 2&1\end{bmatrix}\begin{bmatrix}1-2&3\\ -4&2&5\end{bmatrix}=\begin{bmatrix}2-12&-4+6&6+15\\ 4-20&-8+10&12+25\\ 2-4&-4+2&6+5\end{bmatrix}=\begin{bmatrix}-10&2&21\\ -16&2&37\\ -2&-2&11\end{bmatrix}$$

Clearly AB ≠ BA

and

In the above example both AB and BA are of different order and so AB ≠ BA. But one may think that perhaps AB and BA could be the same if they were of the same order. But it is not so, here we give an example to show that even if AB and BA are of same order they may not be same.

  
  
**Example 14** If $\mathbf{A}=\begin{bmatrix}1&0\\ 0&-1\end{bmatrix}$ and $\mathbf{B}=\begin{bmatrix}0&1\\ 1&0\end{bmatrix}$, then $\mathbf{AB}=\begin{bmatrix}0&1\\ -1&0\end{bmatrix}$.  
  
and $\mathbf{BA}=\begin{bmatrix}0&-1\\ 1&0\end{bmatrix}$. Clearly $\mathbf{AB}\neq\mathbf{BA}$.  
  

Thus matrix multiplication is not commutative.

A**Note** This does not mean that AB ≠ BA for every pair of matrices A, B for which AB and BA, are defined. For instance,

If $\mathbf{A=}\begin{bmatrix}1&0\\ 0&2\end{bmatrix}$, $\mathbf{B=}\begin{bmatrix}3&0\\ 0&4\end{bmatrix}$, then $\mathbf{AB=BA=}\begin{bmatrix}3&0\\ 0&8\end{bmatrix}$

Observe that multiplication of diagonal matrices of same order will be commutative.

#### **Zero matrix as the product of two non zero matrices**

We know that, for real numbers *a*, *b* if *ab* = 0, then either *a* = 0 or *b* = 0. This need not be true for matrices, we will observe this through an example.

  
  
**Example 15**: Find $\mathbf{AB}$, if $\mathbf{A=}\begin{bmatrix}0&-1\\ 0&2\end{bmatrix}$ and $\mathbf{B=}\begin{bmatrix}3&5\\ 0&0\end{bmatrix}$.  
  
**Solution** We have $\mathbf{AB=}\begin{bmatrix}0&-1\\ 0&2\end{bmatrix}\begin{bmatrix}3&5\\ 0&0\end{bmatrix}=\begin{bmatrix}0&0\\ 0&0\end{bmatrix}$.  
  

Thus, if the product of two matrices is a zero matrix, it is not necessary that one of the matrices is a zero matrix.

### **3.4.6** *Properties of multiplication of matrices*

The multiplication of matrices possesses the following properties, which we state without proof.

- 1. **The associative law** For any three matrices A, B and C. We have
(AB) C = A (BC), whenever both sides of the equality are defined.

- 2. **The distributive law** For three matrices A, B and C.
(i) A (B+C) = AB + AC

- (ii) (A+B) C = AC + BC, whenever both sides of equality are defined.
- 3. **The existence of multiplicative identity** For every square matrix A, there exist an identity matrix of same order such that IA = AI = A.

Now, we shall verify these properties by examples.

**Example 16** If 1 1 1 1 3 1 2 3 4 A 2 0 3 , B 0 2 and C 2 0 2 1 3 1 2 1 4 − − = = = − − − , find

A(BC), (AB)C and show that (AB)C = A(BC).

**Solution** We have 1 1 1 1 3 1 0 1 3 2 4 2 1 AB 2 0 3 0 2 2 0 3 6 0 12 1 18 3 1 2 1 4 3 0 2 9 2 8 1 15 − + + + − = = + − + + = − − − + − − + (AB) (C) 2 1 2 2 4 0 6 2 8 1 1 2 3 4 1 18 1 36 2 0 3 36 4 18 2 0 2 1 1 15 1 30 2 0 3 30 4 15 + + − − + − = − = − + − + − − + − + + − − + = 4 4 4 7 35 2 39 22 31 2 27 11 − − − − Now BC = 1 3 1 6 2 0 3 6 4 3 1 2 3 4 0 2 0 4 0 0 0 4 0 2 2 0 2 1 1 4 1 8 2 0 3 8 4 4 + + − − + − = + + − + − − − + − + − − + = 7 2 3 1 4 0 4 2 7 2 11 8 − − − − − Therefore A(BC) = 1 1 1 7 2 3 1 2 0 3 4 0 4 2 3 1 2 7 2 11 8 − − − − − − − = 7 4 7 2 0 2 3 4 11 1 2 8 14 0 21 4 0 6 6 0 33 2 0 24 21 4 14 6 0 4 9 4 22 3 2 16 + − + + − − + − + − + + + − − + − − + + − + + − − + − − − + = 4 4 4 7 35 2 39 22 31 2 27 11 − − − − . Clearly, (AB) C = A (BC)

  
  
**Example 17**: If $\mathbf{A=}\begin{bmatrix}0&6&7\\ -6&0&8\\ 7&-8&0\end{bmatrix},\mathbf{B=}\begin{bmatrix}0&1&1\\ 1&0&2\\ 1&2&0\end{bmatrix},\mathbf{C=}\begin{bmatrix}2\\ -2\\ 3\end{bmatrix}$

Calculate AC, BC and (A + B)C. Also, verify that (A + B)C = AC + BC

**Solution** Now, 0 7 8 A +B 5 0 10 8 6 0 = − − So (A + B) C = 0 7 8 2 0 14 24 10 5 0 10 2 10 0 30 20 8 6 0 3 16 12 0 28 − + − − = − + + = − + + Further AC = 0 6 7 2 0 12 21 9 6 0 8 2 12 0 24 12 7 8 0 3 14 16 0 30 − + − − = − + + = − + + and BC = 0 1 1 2 0 2 3 1 1 0 2 2 2 0 6 8 1 2 0 3 2 4 0 2 − + − = + + = − + − So AC + BC = 9 1 10 12 8 20 30 2 28 + = − Clearly, (A + B) C = AC + BC **Example 18** If 1 2 3 A 3 2 1 4 2 1 = − , then show that A3 – 23A – 40 I = O **Solution** We have 2 1 2 3 1 2 3 19 4 8 A A.A 3 2 1 3 2 1 1 12 8 4 2 1 4 2 1 14 6 15 = = − − = 

So  
  

$$\text{A}^{3}=\text{A}\,\text{A}^{2}=\begin{bmatrix}1&2&3\\ 3&-2&1\\ 4&2&1\end{bmatrix}\begin{bmatrix}19&4&8\\ 1&12&8\\ 14&6&15\end{bmatrix}=\begin{bmatrix}63&46&69\\ 69&-6&23\\ 92&46&63\end{bmatrix}$$

Now

A3 – 23A – 40I = 63 46 69 1 2 3 1 0 0 69 6 23 – 23 3 2 1 – 40 0 1 0 92 46 63 4 2 1 0 0 1 − − = 63 46 69 23 46 69 40 0 0 69 6 23 69 46 23 0 40 0 92 46 63 92 46 23 0 0 40 − − − − − + − − + − − − − − = 63 23 40 46 46 0 69 69 0 69 69 0 6 46 40 23 23 0 92 92 0 46 46 0 63 23 40 − − − + − + − + − + − − + − + − + − − = 0 0 0 0 0 0 O 0 0 0 = 

**Example 19** In a legislative assembly election, a political group hired a public relations firm to promote its candidate in three ways: telephone, house calls, and letters. The cost per contact (in paise) is given in matrix A as

|  |  |  |  | Telephone Housecall |
| --- | --- | --- | --- | --- |
| A = |  | 100 |  |  |
|  |    | Cost per contact 40 50 |    | Letter |

The number of contacts of each type made in two cities X and Y is given by

  
  
\begin{tabular}{c c c} \multicolumn{2}{c}{Telphouse} & \multicolumn{2}{c}{Houscall} & \multicolumn{2}{c}{Letter} \\ \multicolumn{2}{c}{B = } & 1000 & 500 & 5000 \\ \multicolumn{2}{c}{3000 & 1000 & 10,000 } & $\rightarrow$Y \\ \end{tabular}. Find the total amount spent by the group in the two \\ \end{tabular}  
  

cities X and Y.

**Solution** We have

BA = 40,000 50,000 250,000 X 120,000 +100,000 +500,000 Y + + → → = 340,000 X 720,000 Y → →

So the total amount spent by the group in the two cities is 340,000 paise and 720,000 paise, i.e., `3400 and ` 7200, respectively.

**EXERCISE 3.2**

- **1.** Let 2 4 1 3 2 5 A , B , C 3 2 2 5 3 4 − = = = −
Find each of the following:

- (i) A + B (ii) A B (iii) 3A C
- (iv) AB (v) BA
- **2.** Compute the following:

(i) $\begin{bmatrix}a&b\\ -b&a\end{bmatrix}+\begin{bmatrix}a&b\\ b&a\end{bmatrix}$. (ii) $\begin{bmatrix}a^{2}+b^{2}-b^{2}+c^{2}\\ a^{2}+c^{2}&a^{2}+b^{2}\end{bmatrix}+\begin{bmatrix}2ab&2bc\\ -2ac&-2ab\end{bmatrix}$. (iii) $\begin{bmatrix}-1&4&-6\\ 8&5&(16)\\ 2&8&5\end{bmatrix}+\begin{bmatrix}12&7&6\\ 8&0&5\\ 3&2&(4)\end{bmatrix}$. (iv) $\begin{bmatrix}\cos^{2}x&\sin^{2}x\\ \sin^{2}x&\cos^{2}x\end{bmatrix}+\begin{bmatrix}\sin^{2}x&\cos^{2}x\\ \cos^{2}x&\sin^{2}x\end{bmatrix}$.  
  

- **3.** Compute the indicated products.
(i) $\begin{bmatrix}a&b\\ -b&a\end{bmatrix}\begin{bmatrix}a&b\\ b&a\end{bmatrix}$ (ii) $\begin{bmatrix}1\\ 2\\ 3\end{bmatrix}\begin{bmatrix}2&3&4\end{bmatrix}$ (iii) $\begin{bmatrix}1&-2\\ 2&3&1\end{bmatrix}\begin{bmatrix}1&2&3\\ 2&3&1\end{bmatrix}$ (iv) $\begin{bmatrix}2&3&4\\ 3&-4&5\\ 4&5&6\end{bmatrix}\begin{bmatrix}1&-3&5\\ 0&2&4\\ 3&0&5\end{bmatrix}$ (v) $\begin{bmatrix}2&1\\ 3&2\\ -1&1\end{bmatrix}\begin{bmatrix}1&0&1\\ -1&2&1\end{bmatrix}$ (vi) $\begin{bmatrix}3&-1&3\\ -1&0&2\end{bmatrix}\begin{bmatrix}2&-3\\ 1&0\\ 3&1\end{bmatrix}$

**4.** If 1 2 3 3 1 2 4 1 2 A 5 0 2 , B 4 2 5 and C 0 3 2 1 1 1 2 0 3 1 2 3 − − = = = − − , then compute (A+B) and (B – C). Also, verify that A + (B – C) = (A + B) – C. **5.** If 2 5 2 3 1 1 3 3 5 5 1 2 4 1 2 4 A and B 3 3 3 5 5 5 7 2 7 6 2 2 3 3 5 5 5 = = , then compute 3A – 5B. **6.** Simplify cos sin sin cos cos + sin sin cos cos sin θ θ θ − θ θ θ − θ θ θ θ **7.** Find X and Y, if (i) 7 0 3 0 X + Y and X – Y 2 5 0 3 = = (ii) 2 3 2 2 2X + 3Y and 3X 2Y 4 0 1 5 − = + = − **8.** Find X, if Y = 3 2 1 4 and 2X + Y = 1 0 3 2 − **9.** Find *x* and *y*, if 1 3 0 5 6 2 0 1 2 1 8 *y x* + = **10.** Solve the equation for *x*, *y*, *z* and *t*, if 1 1 3 5 2 3 3 0 2 4 6 *x z y t* − + = **11.** If 2 1 10 3 1 5 *x y* − + = , find the values of *x* and *y*. **12.** Given 6 4 3 1 2 3 *x y x x y z w w z w* + = + − + , find the values of *x*, *y*, *z* and *w*.

  
  
**13.**: If $\mathrm{F}\left(x\right)=\left[\begin{array}{ccc}\cos x&-\sin x&0\\ \sin x&\cos x&0\\ 0&0&1\end{array}\right]$, show that $\mathrm{F}(x)\mathrm{F}(y)=\mathrm{F}(x+y)$.  
  

**14.** Show that

(i) 5 1 2 1 2 1 5 1 6 7 3 4 3 4 6 7 − − ≠ (ii) 1 2 3 1 1 0 1 1 0 1 2 3 0 1 0 0 1 1 0 1 1 0 1 0 1 1 0 2 3 4 2 3 4 1 1 0 − − − ≠ − **15.** Find A2 – 5A + 6I, if 2 0 1 A 2 1 3 1 1 0 = − **16.** If 1 0 2 A 0 2 1 2 0 3 = , prove that A3 – 6A2 + 7A + 2I = 0 **17.** If 3 2 1 0 A and I= 4 2 0 1 − = − , find *k* so that A2 = *k*A – 2I **18.** If 0 tan 2 A tan 0 2 α − = α and I is the identity matrix of order 2, show that I + A = (I – A) cos sin sin cos α − α α α

- **19.** A trust fund has ` 30,000 that must be invested in two different types of bonds. The first bond pays 5% interest per year, and the second bond pays 7% interest per year. Using matrix multiplication, determine how to divide ` 30,000 among the two types of bonds. If the trust fund must obtain an annual total interest of: (a) `1800 (b) `2000
- **20.** The bookshop of a particular school has 10 dozen chemistry books, 8 dozen physics books, 10 dozen economics books. Their selling prices are `80, `60 and ` 40 each respectively. Find the total amount the bookshop will receive from selling all the books using matrix algebra.
Assume X, Y, Z, W and P are matrices of order 2 × *n*, 3 × *k*, 2 × *p*, *n* × 3 and *p* × *k*, respectively. Choose the correct answer in Exercises 21 and 22.

- **21.** The restriction on *n*, *k* and *p* so that PY + WY will be defined are:
	- (A) *k* = 3, *p* = *n* (B) *k* is arbitrary, *p* = 2
	- (C) *p* is arbitrary, *k* = 3 (D) *k* = 2, *p* = 3
- **22.** If *n* = *p*, then the order of the matrix 7X 5Z is: (A) *p* × 2 (B) 2 × *n* (C) *n* × 3 (D) *p* × *n*

#### **3.5. Transpose of a Matrix**

In this section, we shall learn about transpose of a matrix and special types of matrices such as symmetric and skew symmetric matrices.

**Definition 3** If A = [*aij*] be an *m* × *n* matrix, then the matrix obtained by interchanging the rows and columns of A is called the *transpose* of A. Transpose of the matrix A is denoted by A′ or (AT ). In other words, if A = [*aij*] *m* × *n* , then A′ = [*aji*] *n* × *m* . For example,

if 2 3 3 2 3 5 3 3 0 A 3 1 , then A 1 5 1 0 1 5 5 × × = ′ = − −

#### *3.5.1 Properties of transpose of the matrices*

We now state the following properties of transpose of matrices without proof. These may be verified by taking suitable examples.

For any matrices A and B of suitable orders, we have

- (i) (A′)′ = A, (ii) (*k*A)′ = *k*A′ (where *k* is any constant)
- (iii) (A + B)′ = A′ + B′ (iv) (A B)′ = B′ A′

**Example 20** If 3 3 2 2 1 2 A and B 4 2 0 1 2 4 − = = , verify that (i) (A′)′ = A, (ii) (A + B)′ = A′ + B′,

- (iii) (*k*B)′ = *k*B′, where *k* is any constant.
#### **Solution**

- (i) We have

$$\mathbf{A}={\left[\begin{array}{l l l}{3}&{{\sqrt{3}}}&{2}\\ {4}&{2}&{0}\end{array}\right]}\Rightarrow\mathbf{A}^{\prime}={\left[\begin{array}{l l}{3}&{4}\\ {{\sqrt{3}}}&{2}\\ {2}&{0}\end{array}\right]}\Rightarrow\left(\mathbf{A}^{\prime}\right)^{\prime}={\left[\begin{array}{l l l}{3}&{{\sqrt{3}}}&{2}\\ {4}&{2}&{0}\end{array}\right]}=\mathbf{A}$$

Thus (A′)′ = A

- (ii) We have
A = 3 3 2 , 4 2 0 B = 2 1 2 5 3 1 4 A B 1 2 4 5 4 4 − − ⇒ + = Therefore (A + B)′ = 5 5 3 1 4 4 4 − Now A′ = 3 4 2 1 3 2 , B 1 2 , 2 0 2 4 ′ = − So A′ + B′ = 5 5 3 1 4 4 4 − Thus (A + B)′ = A′ + B′ (iii) We have *k*B *= k* 2 1 2 2 2 1 2 4 2 4 *k k k k k k* − − = Then (*k*B)′ = 2 2 1 2 1 2 B 2 4 2 4 *k k k k k k k k* − = − = ′ 

Thus (*k*B)′ = *k*B′

  
  
**Example 21**: If $\,\,\mathrm{A}=\!\left[\begin{array}{c}-2\\ 4\\ 5\end{array}\right]$, $\,\mathrm{B}=\!\left[\begin{array}{cc}1&3&-6\end{array}\right]$, verify that $(\,\mathrm{AB})^{\prime}=\mathrm{B}^{\prime}\mathrm{A}^{\prime}$.  
  

**Solution** We have

$$\mathbf{A}={\left[\begin{array}{l}{-2}\\ {4}\\ {5}\end{array}\right]},\mathbf{B}=\left[1\quad3\quad-6\right]$$

$$\operatorname{then}$$

then AB = [ ] 2 4 1 3 6 5 − − = 2 6 12 4 12 24 5 15 30 − − − − 

Now A′ = [–2 4 5] ,

$\mathbf{B^{\prime}A^{\prime}=\left[\begin{array}{c}1\\ 3\end{array}\right]\left[\begin{array}{c}-2\\ 4\end{array}\right]=\left[\begin{array}{c}-2\\ 4\end{array}\right]$  
  
$\mathbf{B^{\prime}A^{\prime}=\left[\begin{array}{c}1\\ 3\end{array}\right]\left[\begin{array}{c}-2\\ 4\end{array}\right]=\left[\begin{array}{c}-2\\ 4\end{array}\right]$  

1

 

B 3

′ =

Clearly (AB)′ = B′A′

### **3.6 Symmetric and Skew Symmetric Matrices**

**Definition 4** A square matrix A = [*aij*] is said to be *symmetric* if A′ = A, that is, [*aij*] = [*aji*] for all possible values of *i* and *j*.

For example A = $\begin{bmatrix}\sqrt{3}&2&3\\ 2&-1.5&-1\\ 3&-1&1\end{bmatrix}$ is a symmetric matrix as A' = A.  
  

**Definition 5** A square matrix A = [*aij*] is said to be *skew symmetric* matrix if A′ = – A, that is *aji* = – *aij* for all possible values of *i* and *j*. Now, if we put *i* = *j*, we have *aii* = – *aii*. Therefore 2*aii* = 0 or *aii* = 0 for all *i*'s.

This means that all the diagonal elements of a skew symmetric matrix are zero.

For example, the matrix $\,\mathbf{B}=\begin{bmatrix}0&e&f\\ -e&0&g\\ -f&-g&0\end{bmatrix}$ is a skew symmetric matrix as $\mathbf{B}^{\prime}=-\mathbf{B}$.  
  

Now, we are going to prove some results of symmetric and skew-symmetric matrices.

**Theorem 1** For any square matrix A with real number entries, A + A′ is a symmetric matrix and A – A′ is a skew symmetric matrix.

**Proof** Let B = A + A′, then

B′ = (A + A′)′ = A′ + (A′)′ (as (A + B)′ = A′ + B′) = A′ + A (as (A′)′ = A) = A + A′ (as A + B = B + A) = B Therefore B = A + A′ is a symmetric matrix Now let C = A – A′ C′ = (A – A′)′ = A′ – (A′)′ (Why?) = A′ – A (Why?) = – (A – A′) = – C Therefore C = A – A′ is a skew symmetric matrix.

**Theorem 2** Any square matrix can be expressed as the sum of a symmetric and a skew symmetric matrix.

**Proof** Let A be a square matrix, then we can write

$$\mathbf{A}={\frac{1}{2}}(\mathbf{A}+\mathbf{A^{\prime}})+{\frac{1}{2}}\left(\mathbf{A}-\mathbf{A^{\prime}}\right)$$

From the Theorem 1, we know that (A + A′) is a symmetric matrix and (A – A′) is a skew symmetric matrix. Since for any matrix A, (*k*A)′ = *k*A′, it follows that 1 (A A ) 2 + ′

is symmetric matrix and 1 (A A ) 2 − ′ is skew symmetric matrix. Thus, any square matrix can be expressed as the sum of a symmetric and a skew symmetric matrix.

**Example 22** Express the matrix 2 2 4 B 1 3 4 1 2 3 − − = − − − as the sum of a symmetric and a skew symmetric matrix.

**Solution** Here

$$\text{B}^{\prime}=\begin{bmatrix}2&-1&1\\ -2&3&-2\\ -4&4&-3\end{bmatrix}$$
  
  
Let  
  

$$\text{P}=\frac{1}{2}\left(\text{B}+\text{B}^{\prime}\right)=\frac{1}{2}\begin{bmatrix}4&-3&-3\\ -3&6&2\\ -3&2&-6\end{bmatrix}=\begin{bmatrix}2&-3&-3\\ -3&2&-6\\ -3&2&-6\end{bmatrix},$$
  
  
Now  
  

$$\text{P}^{\prime}=\begin{bmatrix}2&-3&-3\\ -3&2&-6\end{bmatrix}=\text{P}$$
  
  
Thus  
  

$$\text{P}=\frac{1}{2}\left(\text{B}+\text{B}^{\prime}\right)$$
  
  
is a symmetric matrix.  
  

$$\begin{bmatrix}0&\frac{-1}{\gamma}&\frac{-5}{\gamma}\end{bmatrix}$$

Also, let  
  

$$Q=\frac{1}{2}\left(\text{B}-\text{B}^{\prime}\right)=\frac{1}{2}\left[\begin{array}{ccc}0&-1&-5\\ 1&0&6\\ 5&-6&0\end{array}\right]=\left[\begin{array}{ccc}0&2&2\\ 1&0&3\\ 5&-3&0\end{array}\right]$$

Then Q′ =

$$\left[{\begin{array}{l l l}{0}&{{\frac{1}{2}}}&{{\frac{5}{3}}}\\ {-1}&{0}&{-3}\\ {{\frac{-5}{2}}}&{3}&{0}\end{array}}\right]=-\,\mathbf{Q}$$

Thus Q = 1 (B – B ) 2 ′ is a skew symmetric matrix.

| − | − | − | − | 3 | 3 | 1 | 5 |  |  |  |  | 2 | 0 |  |  |  |  | 2 | 2 | 2 | 2 |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| − | − | 2 | 2 | 4 |  |  |  |  |  |  | − | 3 | 1 |  |  |  |  |  | Now | = | + | = − | = | P + Q | 3 | 1 | 0 | 3 | 1 | 3 | 4 | B |
|  |  |  |  |  |  | 2 | 2 |  |  | − | − | 1 | 2 | 3 |  |  | − | 3 | 5 |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | − | − | 1 | 3 | 3 | 0 |  |  |  |  | 2 | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

Thus, B is represented as the sum of a symmetric and a skew symmetric matrix.

# **EXERCISE 3.3**

- **1.** Find the transpose of each of the following matrices:
(i) 5 1 2 1 − (ii) 1 1 2 3 − (iii) 1 5 6 3 5 6 2 3 1 − − **2.** If 1 2 3 4 1 5 A 5 7 9 and B 1 2 0 2 1 1 1 3 1 − − − = = − , then verify that (i) (A + B)′ = A′ + B′, (ii) (A – B)′ = A′ – B′ **3.** If 3 4 1 2 1 A 1 2 and B 1 2 3 0 1 − ′ = − = , then verify that (i) (A + B)′ = A′ + B′ (ii) (A – B)′ = A′ – B′

**4.** If 2 3 1 0 A and B 1 2 1 2 − − ′ = = , then find (A + 2B)′ **5.** For the matrices A and B, verify that (AB)′ = B′A′, where (i) [ ] 1 A 4 , B 1 2 1 3 = − = − (ii) [ ] 0 A 1 , B 1 5 7 2 = = **6.** If (i) cos sin A sin cos α α = − α α , then verify that A′ A = I (ii) If sin cos A cos sin α α = − α α , then verify that A′ A = I **7.** (i) Show that the matrix 1 1 5 A 1 2 1 5 1 3 − = − is a symmetric matrix. (ii) Show that the matrix 0 1 1 A 1 0 1 1 1 0 − = − − is a skew symmetric matrix. **8.** For the matrix 1 5 A 6 7 = , verify that (i) (A + A′) is a symmetric matrix (ii) (A – A′) is a skew symmetric matrix 0 *a b* 

  
  
**9.**: Find $\frac{1}{2}(\mathbf{A}+\mathbf{A}^{\prime})$ and $\frac{1}{2}(\mathbf{A}-\mathbf{A}^{\prime})$, when $\mathbf{A}=\begin{pmatrix}\mathbf{0}&\mathbf{a}&\mathbf{0}\\ -\mathbf{a}&\mathbf{0}&\mathbf{c}\\ -\mathbf{b}&-\mathbf{c}&\mathbf{0}\end{pmatrix}$

- **10.** Express the following matrices as the sum of a symmetric and a skew symmetric matrix:
(i) $\begin{bmatrix}3&5\\ 1&-1\end{bmatrix}$ (ii) $\begin{bmatrix}6&-2&2\\ -2&3&-1\\ 2&-1&3\end{bmatrix}$  
  
(iii) $\begin{bmatrix}3&3&-1\\ -2&-2&1\\ -4&-5&2\end{bmatrix}$ (iv) $\begin{bmatrix}1&5\\ -1&2\end{bmatrix}$

Choose the correct answer in the Exercises 11 and 12.

- **11.** If A, B are symmetric matrices of same order, then AB BA is a
	- (A) Skew symmetric matrix (B) Symmetric matrix
		-
- (C) Zero matrix (D) Identity matrix **12.** If cos sin A , sin cos α − α = α α and A + A′ = I, then the value of α is (A) 6 π (B) 3 π (C) π (D) 3 2 π

# **3.7 Invertible Matrices**

**Definition 6** If A is a square matrix of order *m*, and if there exists another square matrix B of the same order *m*, such that AB = BA = I, then B is called the *inverse* matrix of A and it is denoted by A– 1. In that case A is said to be invertible.

For example, let  
  

$$\text{A}=\begin{bmatrix}2&3\\ 1&2\end{bmatrix}\text{and}\text{B}=\begin{bmatrix}2&-3\\ -1&2\end{bmatrix}\text{be two matrices.}$$
  
  
Now  
  

$$\text{AB}=\begin{bmatrix}2&3\\ 1&2\end{bmatrix}\begin{bmatrix}2&-3\\ -1&2\end{bmatrix}$$
 
$$=\begin{bmatrix}4-3&-6+6\\ 2-2&-3+4\end{bmatrix}=\begin{bmatrix}1&0\\ 0&1\end{bmatrix}=1$$
  
  
Also  
  

$$\text{BA}=\begin{bmatrix}1&0\\ 0&1\end{bmatrix}=1\text{.Thus B is the inverse of A,in other words B}=\text{A}^{-1}\text{and A is inverse of B,i.e.,A}=\text{B}^{-1}$$

# A**Note**

- 1. A rectangular matrix does not possess inverse matrix, since for products BA and AB to be defined and to be equal, it is necessary that matrices A and B should be square matrices of the same order.
- 2. If B is the inverse of A, then A is also the inverse of B.

**Theorem 3** (Uniqueness of inverse) Inverse of a square matrix, if it exists, is unique. **Proof** Let A = [*aij*] be a square matrix of order *m*. If possible, let B and C be two inverses of A. We shall show that B = C.

Since B is the inverse of A

AB = BA = I 

Since C is also the inverse of A

$$Thus

\begin{array}{c}\mbox{AC}=\mbox{CA}=\mbox{I}^{\mbox{\tiny\circ}}\\ \mbox{B}=\mbox{BI}=\mbox{B}(\mbox{AC})=(\mbox{BA}).\mbox{C}=\mbox{IC}=\mbox{C}\end{array}$$

**Theorem 4** If A and B are invertible matrices of the same order, then (AB)–1 = B–1 A–1 . **Proof** From the definition of inverse of a matrix, we have

(AB) (AB)–1 = 1 or A–1 (AB) (AB)–1 = A–1I (Pre multiplying both sides by A–1) or (A–1A) B (AB)–1 = A–1 (Since A–1 I = A–1) or IB (AB)–1 = A–1 or B (AB)–1 = A–1 or B–1 B (AB)–1 = B–1 A–1 or I (AB)–1 = B–1 A–1 Hence (AB)–1 = B–1 A–1

**EXERCISE 3.4**

- **1.** Matrices A and B will be inverse of each other only if

$$\mathbf{(A)}\ \mathbf{A}\mathbf{B}=\mathbf{B}\mathbf{A}\ \mathbf{(B)}\ \mathbf{A}\mathbf{B}=\mathbf{B}\mathbf{A}=\mathbf{0}$$

(C) AB = 0, BA = I (D) AB = BA = I 

## *Miscellaneous Examples*

  
  
**Example 23**: If $\mathbf{A}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix}$, then prove that $\mathbf{A}^{n}=\begin{bmatrix}\cos n\theta&\sin n\theta\\ -\sin n\theta&\cos n\theta\end{bmatrix}$, $n\in\mathbf{N}$.  
  

**Solution** We shall prove the result by using principle of mathematical induction.

We have  
  

$$\begin{array}{c}\text{P}(n):\text{If}\;\;\text{A}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix},\text{then}\;\;\text{A}^{n}=\begin{bmatrix}\cos n\theta&\sin n\theta\\ -\sin n\theta&\cos n\theta\end{bmatrix},\,n\in\text{N}\\ \cdot\\ \text{P}(1):\text{A}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix},\text{so}\;\;\text{A}^{1}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix}.\end{array}$$
  
  
Therefore, the result is true for $n=1$.  
  

Therefore, the result is true for *n* = 1. Let the result be true for *n* = *k*. So

$\mathrm{P}(k):\mathrm{A}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix}$, then $\mathrm{A}^{k}=\begin{bmatrix}\cos k\theta&\sin k\theta\\ -\sin k\theta&\cos k\theta\end{bmatrix}$

Now, we prove that the result holds for *n* = *k* +1

Now A*k* + 1 = cos sin cos sin A A sin cos sin cos *k k k k k* θ θ θ θ ⋅ = − θ θ − θ θ = cos cos – sin sin cos sin sin cos sin cos cos sin sin sin cos cos *k k k k k k k k* θ θ θ θ θ θ + θ θ − θ θ + θ θ − θ θ + θ θ = cos( ) sin ( ) cos( 1) sin ( 1) sin ( ) cos( ) sin ( 1) cos( 1) *k k k k k k k k* θ + θ θ + θ + θ + θ = − θ + θ θ + θ − + θ + θ

Therefore, the result is true for *n* = *k* + 1. Thus by principle of mathematical induction,

we have cos sin A sin cos *n n n n n* θ θ = − θ θ , holds for all natural numbers.

**Example 24** If A and B are symmetric matrices of the same order, then show that AB is symmetric if and only if A and B commute, that is AB = BA.

**Solution** Since A and B are both symmetric matrices, therefore A′ = A and B′ = B.

Let AB be symmetric, then (AB)′ = AB

But (AB)′ = B′A′= BA (Why?) Therefore BA = AB

Conversely, if AB = BA, then we shall show that AB is symmetric.

Now (AB)′ = B′A′

= B A (as A and B are symmetric)

$$=\mathrm{AB}$$

Hence AB is symmetric.

**Example 25** Let 2 1 5 2 2 5 A , B , C 3 4 7 4 3 8 − = = = . Find a matrix D such that CD – AB = O.

**Solution** Since A, B, C are all square matrices of order 2, and CD – AB is well defined, D must be a square matrix of order 2.

Let D = *a b c d* . Then CD – AB = 0 gives 2 5 2 1 5 2 3 8 3 4 7 4 *a b c d* − − = O or 2 5 2 5 3 0 3 8 3 8 43 22 *a c b d a c b d* + + − + + = 0 0 0 0 or 2 5 3 2 5 3 8 43 3 8 22 *a c b d a c b d* + − + + − + − = 0 0 0 0 

By equality of matrices, we get

$2a+5c-3=0$

$3a+8c-43=0$

$2b+5d=0$

$$3b+8d-22=0$$

Solving (1) and (2), we get *a* = –191, *c* = 77. Solving (3) and (4), we get *b* = – 110, *d* = 44.

Therefore D =

$$\mathbf{D}={\overset{\cdot}{\begin{bmatrix}a&b\\ c&d\end{bmatrix}}}={\overset{\cdot}{\begin{bmatrix}-191&-110\\ 77&44\end{bmatrix}}}$$

# *Miscellaneous Exercise on Chapter 3*

- **1.** If A and B are symmetric matrices, prove that AB BA is a skew symmetric matrix.
- **2.** Show that the matrix B′AB is symmetric or skew symmetric according as A is symmetric or skew symmetric.
- **3.** Find the values of *x*, *y*, *z* if the matrix 0 2 A *y z x y z x y z* = − − satisfy the equation

A′A = I.

$$

**4.** For what values of x:[1-2-1]2012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012012$$

  
  
**5.** If $\mathbf{A}=\begin{bmatrix}3&1\\ -1&2\end{bmatrix}$, show that $\mathbf{A}^{2}-5\mathbf{A}+7\mathbf{I}=0$.  
  

- **6.** Find *x*, if [ ] 1 0 2 5 1 0 2 1 4 O 2 0 3 1 *x x* − − =
- **7.** A manufacturer produces three products *x*, *y*, *z* which he sells in two markets. Annual sales are indicated below:

| Market |  | Products |  |
| --- | --- | --- | --- |
| I | 10,000 | 2,000 | 18,000 |
| II | 6,000 | 20,000 | 8,000 |

- (a) If unit sale prices of *x*, *y* and *z* are ` 2.50, ` 1.50 and ` 1.00, respectively, find the total revenue in each market with the help of matrix algebra.
- (b) If the unit costs of the above three commodities are ` 2.00, ` 1.00 and 50 paise respectively. Find the gross profit.

  
  
**8.** Find the matrix X so that $\mathbf{X}\begin{bmatrix}1&2&3\\ 4&5&6\end{bmatrix}=\begin{bmatrix}-7&-8&-9\\ 2&4&6\end{bmatrix}$

Choose the correct answer in the following questions:

- **9.** If A = is such that A² = I, then (A) 1 + α² + βγ = 0 (B) 1 – α² + βγ = 0 (C) 1 – α² – βγ = 0 (D) 1 + α² – βγ = 0 *α β γ α*−
**10.** If the matrix A is both symmetric and skew symmetric, then

- (A) A is a diagonal matrix (B) A is a zero matrix
- (C) A is a square matrix (D) None of these

**11.** If A is square matrix such that A2 = A, then (I + A)³ – 7 A is equal to (A) A (B) I – A (C) I (D) 3A

#### *Summary*

- Æ A matrix is an ordered rectangular array of numbers or functions.
- Æ A matrix having *m* rows and *n* columns is called a matrix of order *m* × *n*.
- Æ [*aij*] *m* × 1 is a column matrix.
- Æ [*aij*] 1 × *n* is a row matrix.
- Æ An *m* × *n* matrix is a square matrix if *m* = *n*.
- Æ A = [*aij*] *m* × *m* is a diagonal matrix if *aij* = 0, when *i* ≠ *j*.
- Æ A = [*aij*] *n* × *n* is a scalar matrix if *aij* = 0, when *i* ≠ *j*, *aij* = *k*, (*k* is some constant), when *i* = *j*.
- Æ A = [*aij*] *n* × *n* is an identity matrix, if *aij* = 1, when *i* = *j*, *aij* = 0, when *i* ≠ *j*.
- Æ A zero matrix has all its elements as zero.
- Æ A = [*aij*] = [*bij*] = B if (i) A and B are of same order, (ii) *aij* = *bij* for all possible values of *i* and *j*.

$\bullet$ **A = $\left[\left[\left.\frac{\partial}{\partial t}\right]_{m}\right.\right]_{m}$ = $\left[\left.\frac{\partial}{\partial t}\right]_{m}$ = \(\left[\left.  
  

$$\begin{array}{r l}{\bullet}&{{}-\mathrm{A}=(-1)\mathrm{A}}\end{array}$$

- Æ A B = A + (–1) B

$$\begin{array}{r l}{\bullet}&{{}\mathrm{A+B=B+A}}\end{array}$$

- Æ (A + B) + C = A + (B + C), where A, B and C are of same order.
- Æ *k*(A + B) = *k*A + *k*B, where A and B are of same order, *k* is constant.
- Æ (*k* + *l*) A = *k*A + *l*A, where *k* and *l* are constant.
- Æ If A = [*aij*] *m* × *n* and B = [*bjk*] *n* × *p* , then AB = C = [*cik*] *m* × *p* , where = =1 *ik ij jk j c a b* ∑

*n*

- Æ (i) A(BC) = (AB)C, (ii) A(B + C) = AB + AC, (iii) (A + B)C = AC + BC
- Æ If A = [*aij*] *m* × *n* , then A′ or AT = [*aji*] *n* × *m*
- Æ (i) (A′)′ = A, (ii) (*k*A)′ = *k*A′, (iii) (A + B)′ = A′ + B′, (iv) (AB)′ = B′A′
- Æ A is a symmetric matrix if A′ = A.
- Æ A is a skew symmetric matrix if A′ = –A.
- Æ Any square matrix can be represented as the sum of a symmetric and a skew symmetric matrix.
- Æ If A and B are two square matrices such that AB = BA = I, then B is the inverse matrix of A and is denoted by A–1 and A is the inverse of B.

**—**v**—**

- Æ Inverse of a square matrix, if it exists, is unique.
![](_page_41_Figure_0.jpeg)

