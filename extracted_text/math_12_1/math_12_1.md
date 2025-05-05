![](_page_0_Picture_0.jpeg)

v*There is no permanent place in the world for ugly mathematics ... . It may be very hard to define mathematical beauty but that is just as true of beauty of any kind, we may not know quite what we mean by a beautiful poem, but that does not prevent us from recognising one when we read it. — G. H. HARDY* v

# **1.1 Introduction**

Recall that the notion of relations and functions, domain, co-domain and range have been introduced in Class XI along with different types of specific real valued functions and their graphs. The concept of the term 'relation' in mathematics has been drawn from the meaning of relation in English language, according to which two objects or quantities are related if there is a recognisable connection or link between the two objects or quantities. Let A be the set of students of Class XII of a school and B be the set of students of Class XI of the same school. Then some of the examples of relations from A to B are

- (i) {(*a*, *b*) ∈ A × B: *a* is brother of *b*},
- (ii) {(*a*, *b*) ∈ A × B: *a* is sister of *b*},
- (iii) {(*a*, *b*) ∈ A × B: age of *a* is greater than age of *b*},
- (iv) {(*a*, *b*) ∈ A × B: total marks obtained by *a* in the final examination is less than the total marks obtained by *b* in the final examination},
- (v) {(*a*, *b*) ∈ A × B: *a* lives in the same locality as *b*}. However, abstracting from this, we define mathematically a relation R from A to B as an arbitrary subset of A × B.

If (*a*, *b*) ∈ R, we say that *a* is related to *b* under the relation R and we write as *a* R *b*. In general, (*a*, *b*) ∈ R, we do not bother whether there is a recognisable connection or link between *a* and *b*. As seen in Class XI, functions are special kind of relations.

In this chapter, we will study different types of relations and functions, composition of functions, invertible functions and binary operations.

**Lejeune Dirichlet (1805-1859)**

# **1.2 Types of Relations**

In this section, we would like to study different types of relations. We know that a relation in a set A is a subset of A × A. Thus, the empty set φ and A × A are two extreme relations. For illustration, consider a relation R in the set A = {1, 2, 3, 4} given by R = {(*a*, *b*): *a* – *b* = 10}. This is the empty set, as no pair (*a*, *b*) satisfies the condition *a* – *b* = 10. Similarly, R′ = {(*a*, *b*) : | *a* – *b* | ≥ 0} is the whole set A × A, as all pairs (*a*, *b*) in A × A satisfy | *a* – *b* | ≥ 0. These two extreme examples lead us to the following definitions.

**Definition 1** A relation R in a set A is called *empty relation*, if no element of A is related to any element of A, i.e., R = φ ⊂ A × A.

**Definition 2**A relation R in a set A is called *universal relation*, if each element of A is related to every element of A, i.e., R = A × A.

Both the empty relation and the universal relation are some times called *trivial relations*.

**Example 1** Let A be the set of all students of a boys school. Show that the relation R in A given by R = {(*a*, *b*) : *a* is sister of *b*} is the empty relation and R′ = {(*a*, *b*) : the difference between heights of *a* and *b* is less than 3 meters} is the universal relation.

**Solution** Since the school is boys school, no student of the school can be sister of any student of the school. Hence, R = φ, showing that R is the empty relation. It is also obvious that the difference between heights of any two students of the school has to be less than 3 meters. This shows that R′ = A × A is the universal relation.

*Remark* In Class XI, we have seen two ways of representing a relation, namely raster method and set builder method. However, a relation R in the set {1, 2, 3, 4} defined by R = {(*a*, *b*) : *b* = *a* + 1} is also expressed as *a* R *b* if and only if *b* = *a* + 1 by many authors. We may also use this notation, as and when convenient.

If (*a*, *b*) ∈ R, we say that *a* is related to *b* and we denote it as *a* R *b*.

One of the most important relation, which plays a significant role in Mathematics, is an *equivalence relation*. To study equivalence relation, we first consider three types of relations, namely reflexive, symmetric and transitive.

**Definition 3** A relation R in a set A is called

- (i) *reflexive*, if (*a*, *a*) ∈ R, for every *a* ∈ A,
- (ii) *symmetric*, if (*a*1 , *a*2 ) ∈ R implies that (*a*2 , *a*1 ) ∈ R, for all *a*1 , *a*2 ∈ A.
- (iii) *transitive*, if (*a*1 , *a*2 ) ∈ R and (*a*2 , *a*3 ) ∈ R implies that (*a*1 , *a*3 )∈ R, for all *a*1 , *a*2 , *a*3 ∈ A.

**Definition 4** A relation R in a set A is said to be an *equivalence relation* if R is reflexive, symmetric and transitive.

**Example 2** Let T be the set of all triangles in a plane with R a relation in T given by R = {(T1 , T2 ) : T1 is congruent to T2 }. Show that R is an equivalence relation.

**Solution** R is reflexive, since every triangle is congruent to itself. Further, (T1 , T2 ) ∈ R ⇒ T1 is congruent to T2 ⇒ T2 is congruent to T1 ⇒ (T2 , T1 ) ∈ R. Hence, R is symmetric. Moreover, (T1 , T2 ), (T2 , T3 ) ∈ R ⇒ T1 is congruent to T2 and T2 is congruent to T3 ⇒ T1 is congruent to T3 ⇒ (T1 , T3 ) ∈ R. Therefore, R is an equivalence relation.

**Example 3** Let L be the set of all lines in a plane and R be the relation in L defined as R = {(L1 , L2 ) : L1 is perpendicular to L2 }. Show that R is symmetric but neither reflexive nor transitive.

**Solution** R is not reflexive, as a line L1 can not be perpendicular to itself, i.e., (L1 , L1 ) ∉ R. R is symmetric as (L1 , L2 ) ∈ R ⇒ L1 is perpendicular to L2 ⇒ L2 is perpendicular to L1 ⇒ (L2 , L1 ) ∈ R. R is not transitive. Indeed, if L1 is perpendicular to L2 and can never be perpendicular to **Fig 1.1**

L2 is perpendicular to L3 , then L1 L3 . In fact, L1 is parallel to L3 , i.e., (L1 , L2 ) ∈ R, (L2 , L3 ) ∈ R but (L1 , L3 ) ∉ R.

**Example 4** Show that the relation R in the set {1, 2, 3} given by R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 3)} is reflexive but neither symmetric nor transitive.

**Solution** R is reflexive, since (1, 1), (2, 2) and (3, 3) lie in R. Also, R is not symmetric, as (1, 2) ∈ R but (2, 1) ∉ R. Similarly, R is not transitive, as (1, 2) ∈ R and (2, 3) ∈ R but (1, 3) ∉ R.

**Example 5** Show that the relation R in the set **Z** of integers given by

R = {(*a, b*) : 2 divides *a* – *b*}

is an equivalence relation.

**Solution** R is reflexive, as 2 divides (*a* – *a*) for all *a* ∈ **Z**. Further, if (*a, b*) ∈ R, then 2 divides *a* – *b*. Therefore, 2 divides *b* – *a*. Hence, (*b*, *a*) ∈ R, which shows that R is symmetric. Similarly, if (*a*, *b*) ∈ R and (*b*, *c*) ∈ R, then *a* – *b* and *b* – *c* are divisible by 2. Now, *a* – *c* = (*a* – *b*) + (*b* – *c*) is even (Why?). So, (*a* – *c*) is divisible by 2. This shows that R is transitive. Thus, R is an equivalence relation in **Z**.

In Example 5, note that all even integers are related to zero, as (0, ± 2), (0, ± 4) etc., lie in R and no odd integer is related to 0, as (0, ± 1), (0, ± 3) etc., do not lie in R. Similarly, all odd integers are related to one and no even integer is related to one. Therefore, the set E of all even integers and the set O of all odd integers are subsets of **Z** satisfying following conditions:

- (i) All elements of E are related to each other and all elements of O are related to each other.
- (ii) No element of E is related to any element of O and vice-versa.
- (iii) E and O are disjoint and **Z** = E ∪ O.

The subset E is called the *equivalence class containing zero* and is denoted by [0]. Similarly, O is the equivalence class containing 1 and is denoted by [1]. Note that [0] ≠ [1], [0] = [2*r*] and [1] = [2*r* + 1], *r* ∈ **Z**. Infact, what we have seen above is true for an arbitrary equivalence relation R in a set X. Given an arbitrary equivalence relation R in an arbitrary set X, R divides X into mutually disjoint subsets A*i* called partitions or subdivisions of X satisfying:

- (i) all elements of A*i* are related to each other, for all *i*.
- (ii) no element of A*i* is related to any element of A*j* , *i* ≠ *j*.
- (iii) ∪ A*j* = X and A*i* ∩ A*j* = φ, *i* ≠ *j*.

The subsets A*i* are called *equivalence classes*. The interesting part of the situation is that we can go reverse also. For example, consider a subdivision of the set **Z** given by three mutually disjoint subsets A1 , A2 and A3 whose union is **Z** with

$\mathrm{A}_{1}=\{x\in\mathbf{Z}:x\text{is a multiple of}3\}=\{...,-6,-3,\,0,\,3,\,6,\,...\}$  
  
$\mathrm{A}_{2}=\{x\in\mathbf{Z}:x-1\text{is a multiple of}3\}=\{...,-5,-2,\,1,\,4,\,7,\,...\}$  
  
$\mathrm{A}_{3}=\{x\in\mathbf{Z}:x-2\text{is a multiple of}3\}=\{...,-4,-1,\,2,\,5,\,8,\,...\}$

Define a relation R in **Z** given by R = {(*a*, *b*) : 3 divides *a* – *b*}. Following the arguments similar to those used in Example 5, we can show that R is an equivalence relation. Also, A1 coincides with the set of all integers in **Z** which are related to zero, A2 coincides with the set of all integers which are related to 1 and A3 coincides with the set of all integers in **Z** which are related to 2. Thus, A1 = [0], A2 = [1] and A3 = [2]. In fact, A1 = [3*r*], A2 = [3*r* + 1] and A3 = [3*r* + 2], for all *r* ∈ **Z**.

**Example 6** Let R be the relation defined in the set A = {1, 2, 3, 4, 5, 6, 7} by R = {(*a*, *b*) : both *a* and *b* are either odd or even}. Show that R is an equivalence relation. Further, show that all the elements of the subset {1, 3, 5, 7} are related to each other and all the elements of the subset {2, 4, 6} are related to each other, but no element of the subset {1, 3, 5, 7} is related to any element of the subset {2, 4, 6}.

**Solution** Given any element *a* in A, both *a* and *a* must be either odd or even, so that (*a*, *a*) ∈ R. Further, (*a*, *b*) ∈ R ⇒ both *a* and *b* must be either odd or even ⇒ (*b*, *a*) ∈ R. Similarly, (*a*, *b*) ∈ R and (*b*, *c*) ∈ R ⇒ all elements *a*, *b*, *c*, must be either even or odd simultaneously ⇒ (*a*, *c*) ∈ R. Hence, R is an equivalence relation. Further, all the elements of {1, 3, 5, 7} are related to each other, as all the elements of this subset are odd. Similarly, all the elements of the subset {2, 4, 6} are related to each other, as all of them are even. Also, no element of the subset {1, 3, 5, 7} can be related to any element of {2, 4, 6}, as elements of {1, 3, 5, 7} are odd, while elements of {2, 4, 6} are even.

## **EXERCISE 1.1**

- **1.** Determine whether each of the following relations are reflexive, symmetric and transitive:
	- (i) Relation R in the set A = {1, 2, 3, ..., 13, 14} defined as

[16] M. C. Gonzalez-Garcia, M.  
  

- (ii) Relation R in the set **N** of natural numbers defined as R = {(*x*, *y*) : *y* = *x* + 5 and *x* < 4}
- (iii) Relation R in the set A = {1, 2, 3, 4, 5, 6} as

R = {(*x*, *y*) : *y* is divisible by *x*}

- (iv) Relation R in the set **Z** of all integers defined as
R = {(*x*, *y*) : *x* – *y* is an integer}

- (v) Relation R in the set A of human beings in a town at a particular time given by
	- (a) R = {(*x*, *y*) : *x* and *y* work at the same place}
	- (b) R = {(*x*, *y*) : *x* and *y* live in the same locality}
	- (c) R = {(*x*, *y*) : *x* is exactly 7 cm taller than *y*}
	- (d) R = {(*x*, *y*) : *x* is wife of *y*}
	- (e) R = {(*x*, *y*) : *x* is father of *y*}
- **2.** Show that the relation R in the set **R** of real numbers, defined as R = {(*a*, *b*) : *a* ≤ *b* 2} is neither reflexive nor symmetric nor transitive.
- **3.** Check whether the relation R defined in the set {1, 2, 3, 4, 5, 6} as R = {(*a*, *b*) : *b = a* + 1} is reflexive, symmetric or transitive.
- **4.** Show that the relation R in **R** defined as R = {(*a*, *b*) : *a* ≤ *b*}, is reflexive and transitive but not symmetric.
- **5.** Check whether the relation R in **R** defined by R = {(*a*, *b*) : *a* ≤ *b* 3} is reflexive, symmetric or transitive.

- **6.** Show that the relation R in the set {1, 2, 3} given by R = {(1, 2), (2, 1)} is symmetric but neither reflexive nor transitive.
- **7.** Show that the relation R in the set A of all the books in a library of a college, given by R = {(*x*, *y*) : *x* and *y* have same number of pages} is an equivalence relation.
- **8.** Show that the relation R in the set A = {1, 2, 3, 4, 5} given by

R = {(*a*, *b*) : |*a* – *b*| is even}, is an equivalence relation. Show that all the elements of {1, 3, 5} are related to each other and all the elements of {2, 4} are related to each other. But no element of {1, 3, 5} is related to any element of {2, 4}.

- **9.** Show that each of the relation R in the set A = {*x* ∈ **Z** : 0 ≤ *x* ≤ 12}, given by
	- (i) R = {(*a*, *b*) : |*a b*| is a multiple of 4}
	- (ii) R = {(*a*, *b*) : *a* = *b*}

is an equivalence relation. Find the set of all elements related to 1 in each case.

- **10.** Give an example of a relation. Which is
	- (i) Symmetric but neither reflexive nor transitive.
	- (ii) Transitive but neither reflexive nor symmetric.
	- (iii) Reflexive and symmetric but not transitive.
	- (iv) Reflexive and transitive but not symmetric.
	- (v) Symmetric and transitive but not reflexive.
- **11.** Show that the relation R in the set A of points in a plane given by R = {(P, Q) : distance of the point P from the origin is same as the distance of the point Q from the origin}, is an equivalence relation. Further, show that the set of all points related to a point P ≠ (0, 0) is the circle passing through P with origin as centre.
- **12.** Show that the relation R defined in the set A of all triangles as R = {(T1 , T2 ) : T1 is similar to T2 }, is equivalence relation. Consider three right angle triangles T1 with sides 3, 4, 5, T2 with sides 5, 12, 13 and T3 with sides 6, 8, 10. Which triangles among T1 , T2 and T3 are related?
- **13.** Show that the relation R defined in the set A of all polygons as R = {(P1 , P2 ) : P1 and P2 have same number of sides}, is an equivalence relation. What is the set of all elements in A related to the right angle triangle T with sides 3, 4 and 5?
- **14.** Let L be the set of all lines in XY plane and R be the relation in L defined as R = {(L1 , L2 ) : L1 is parallel to L2 }. Show that R is an equivalence relation. Find the set of all lines related to the line *y* = 2*x* + 4.
- **15.** Let R be the relation in the set {1, 2, 3, 4} given by R = {(1, 2), (2, 2), (1, 1), (4,4), (1, 3), (3, 3), (3, 2)}. Choose the correct answer.
	- (A) R is reflexive and symmetric but not transitive.
	- (B) R is reflexive and transitive but not symmetric.
	- (C) R is symmetric and transitive but not reflexive.
	- (D) R is an equivalence relation.
- **16.** Let R be the relation in the set **N** given by R = {(*a*, *b*) : *a* = *b* 2, *b* > 6}. Choose the correct answer.

(A) (2, 4) ∈ R (B) (3, 8) ∈ R (C) (6, 8) ∈ R (D) (8, 7) ∈ R

## **1.3 Types of Functions**

The notion of a function along with some special functions like identity function, constant function, polynomial function, rational function, modulus function, signum function etc. along with their graphs have been given in Class XI.

Addition, subtraction, multiplication and division of two functions have also been studied. As the concept of function is of paramount importance in mathematics and among other disciplines as well, we would like to extend our study about function from where we finished earlier. In this section, we would like to study different types of functions.

Consider the functions *f* 1 , *f* 2 , *f* 3 and *f* 4 given by the following diagrams.

In Fig 1.2, we observe that the images of distinct elements of X1 under the function *f* 1 are distinct, but the image of two distinct elements 1 and 2 of X1 under *f* 2 is same, namely *b*. Further, there are some elements like *e* and *f* in X2 which are not images of any element of X1 under *f* 1 , while all elements of X3 are images of some elements of X1 under *f* 3 . The above observations lead to the following definitions:

**Definition 5** A function *f* : X → Y is defined to be *one-one* (or *injective*), if the images of distinct elements of X under *f* are distinct, i.e., for every *x*1 , *x*2 ∈ X, *f*(*x*1 ) = *f*(*x*2 ) implies *x*1 = *x*2 . Otherwise, *f* is called *many-one*.

The function *f* 1 and *f* 4 in Fig 1.2 (i) and (iv) are one-one and the function *f* 2 and *f* 3 in Fig 1.2 (ii) and (iii) are many-one.

**Definition 6** A function *f* : X → Y is said to be *onto* (or *surjective*), if every element of Y is the image of some element of X under *f*, i.e., for every *y* ∈ Y, there exists an element *x* in X such that *f*(*x*) = *y*.

The function *f* 3 and *f* 4 in Fig 1.2 (iii), (iv) are onto and the function *f* 1 in Fig 1.2 (i) is not onto as elements *e*, *f* in X2 are not the image of any element in X1 under *f* 1 .

![](_page_7_Figure_1.jpeg)

**Fig 1.2 (i) to (iv)**

*Remark f* : X → Y is onto if and only if Range of *f* = Y.

**Definition 7** A function *f* : X → Y is said to be *one-one* and *onto* (or *bijective*), if *f* is both one-one and onto.

The function *f* 4 in Fig 1.2 (iv) is one-one and onto.

**Example 7** Let A be the set of all 50 students of Class X in a school. Let *f* : A → **N** be function defined by *f*(*x*) = roll number of the student *x*. Show that *f* is one-one but not onto.

**Solution** No two different students of the class can have same roll number. Therefore, *f* must be one-one. We can assume without any loss of generality that roll numbers of students are from 1 to 50. This implies that 51 in **N** is not roll number of any student of the class, so that 51 can not be image of any element of X under *f*. Hence, *f* is not onto.

**Example 8** Show that the function *f* : **N** → **N**, given by *f*(*x*) = 2*x*, is one-one but not onto.

**Solution** The function *f* is one-one, for *f*(*x*1 ) = *f*(*x*2 ) ⇒ 2*x*1 = 2*x*2 ⇒ *x*1 = *x*2 . Further, *f* is not onto, as for 1 ∈ **N**, there does not exist any *x* in **N** such that *f*(*x*) = 2*x* = 1.

**Example 9** Prove that the function *f* : **R** → **R**, given by *f*(*x*) = 2*x*, is one-one and onto. **Solution** *f* is one-one, as *f*(*x*1 ) = *f*(*x*2 ) ⇒ 2*x*1 = 2*x*2 ⇒ *x*1 = *x*2 . Also, given any real number *y* in R, there exists 2 *y* in R such that *f*( 2 *y* ) = 2 . ( 2 *y* ) = *y*. Hence, *f* is onto.

![](_page_8_Figure_2.jpeg)

**Example 10** Show that the function *f* : **N**→ **N**, given by *f* (1) = *f*(2) = 1 and *f*(*x*) = *x* – 1, for every *x* > 2, is onto but not one-one.

**Solution** *f* is not one-one, as *f*(1) = *f*(2) = 1. But *f* is onto, as given any *y* ∈ **N**, *y* ≠ 1, we can choose *x* as *y* + 1 such that *f*(*y* + 1) = *y* + 1 – 1 = *y*. Also for 1 ∈ **N**, we have *f*(1) = 1.

**Example 11** Show that the function *f* : **R** → **R**, defined as *f*(*x*) = *x* 2 , is neither one-one nor onto.

**Solution** Since *f*(– 1) = 1 = *f*(1), *f* is not oneone. Also, the element – 2 in the co-domain **R** is not image of any element *x* in the domain **R** (Why?). Therefore *f* is not onto.

**Example 12** Show that *f* : **N** → **N**, given by

$$f(x)={\begin{array}{l}{x+1,{\mathrm{if~}}x{\mathrm{~is~odd,}}}\\ {x-1,{\mathrm{if~}}x{\mathrm{~is~even.}}}\end{array}}$$

is both one-one and onto. **Fig 1.4**

![](_page_8_Figure_10.jpeg)

**Solution** Suppose *f*(*x*1 ) = *f*(*x*2 ). Note that if *x*1 is odd and *x*2 is even, then we will have *x*1 + 1 = *x*2 – 1, i.e., *x*2 – *x*1 = 2 which is impossible. Similarly, the possibility of *x*1 being even and *x*2 being odd can also be ruled out, using the similar argument. Therefore, both *x*1 and *x*2 must be either odd or even. Suppose both *x*1 and *x*2 are odd. Then *f*(*x*1 ) = *f*(*x*2 ) ⇒ *x*1 + 1 = *x*2 + 1 ⇒ *x*1 = *x*2 . Similarly, if both *x*1 and *x*2 are even, then also *f*(*x*1 ) = *f*(*x*2 ) ⇒ *x*1 – 1 = *x*2 – 1 ⇒ *x*1 = *x*2 . Thus, *f* is one-one. Also, any odd number 2*r* + 1 in the co-domain **N** is the image of 2*r +* 2 in the domain **N** and any even number 2*r* in the co-domain **N** is the image of 2*r* – 1 in the domain **N**. Thus, *f* is onto.

**Example 13** Show that an onto function *f* : {1, 2, 3} → {1, 2, 3} is always one-one.

**Solution** Suppose *f* is not one-one. Then there exists two elements, say 1 and 2 in the domain whose image in the co-domain is same. Also, the image of 3 under *f* can be only one element. Therefore, the range set can have at the most two elements of the co-domain {1, 2, 3}, showing that *f* is not onto, a contradiction. Hence, *f* must be one-one.

**Example 14** Show that a one-one function *f* : {1, 2, 3} → {1, 2, 3} must be onto.

**Solution** Since *f* is one-one, three elements of {1, 2, 3} must be taken to 3 different elements of the co-domain {1, 2, 3} under *f*. Hence, *f* has to be onto.

*Remark* The results mentioned in Examples 13 and 14 are also true for an arbitrary finite set X, i.e., a one-one function *f* : X → X is necessarily onto and an onto map *f* : X → X is necessarily one-one, for every finite set X. In contrast to this, Examples 8 and 10 show that for an infinite set, this may not be true. In fact, this is a characteristic difference between a finite and an infinite set.

**EXERCISE 1.2**

- **1.** Show that the function *f* : **R**∗ → **R**∗ defined by *f*(*x*) = 1 *x* is one-one and onto,
where **R**∗ is the set of all non-zero real numbers. Is the result true, if the domain **R**∗ is replaced by **N** with co-domain being same as **R**∗ ?

- **2.** Check the injectivity and surjectivity of the following functions:
	- (i) *f* : **N** → **N** given by *f*(*x*) = *x* 2
	- (ii) *f* : **Z** → **Z** given by *f*(*x*) = *x* 2
	- (iii) *f* : **R** → **R** given by *f*(*x*) = *x* 2
	- (iv) *f* : **N** → **N** given by *f*(*x*) = *x* 3
	- (v) *f* : **Z** → **Z** given by *f*(*x*) = *x* 3
- **3.** Prove that the Greatest Integer Function *f* : **R** → **R**, given by *f*(*x*) = [*x*], is neither one-one nor onto, where [*x*] denotes the greatest integer less than or equal to *x*.
- **4.** Show that the Modulus Function *f* : **R** → **R**, given by *f*(*x*) = | *x* |, is neither oneone nor onto, where | *x* | is *x*, if *x* is positive or 0 and | *x* | is – *x*, if *x* is negative.
- **5.** Show that the Signum Function *f* : **R** → **R**, given by

$$f(x)={\begin{cases}1,{\mathrm{if~}}x>0\\ 0,{\mathrm{if~}}x=0\\ 1,{\mathrm{if~}}x<0\end{cases}}$$

is neither one-one nor onto.

- **6.** Let A = {1, 2, 3}, B = {4, 5, 6, 7} and let *f* = {(1, 4), (2, 5), (3, 6)} be a function from A to B. Show that *f* is one-one.
- **7.** In each of the following cases, state whether the function is one-one, onto or bijective. Justify your answer.
	- (i) *f* : **R** → **R** defined by *f*(*x*) = 3 4*x*
	- (ii) *f* : **R** → **R** defined by *f*(*x*) = 1 + *x* 2
- **8.** Let A and B be sets. Show that *f* : A × B → B × A such that *f*(*a*, *b*) = (*b*, *a*) is bijective function.
- **9.** Let *f* : **N** → **N** be defined by *f* (*n*) = *n n n n* + 1 2 2 , , if is odd if is even for all *n* ∈ **N**.

State whether the function *f* is bijective. Justify your answer.

- **10.** Let A = **R** {3} and B = **R** {1}. Consider the function *f* : A → B defined by *f*(*x*) = 2 3 *x x* − − . Is *f* one-one and onto? Justify your answer.
- **11.** Let *f* : **R** → **R** be defined as *f*(*x*) = *x* 4 . Choose the correct answer.
	- (A) *f* is one-one onto (B) *f* is many-one onto
		- (C) *f* is one-one but not onto (D) *f* is neither one-one nor onto.
- **12.** Let *f* : **R** → **R** be defined as *f*(*x*) = 3*x*. Choose the correct answer.
	- (A) *f* is one-one onto (B) *f* is many-one onto
	- (C) *f* is one-one but not onto (D) *f* is neither one-one nor onto.

## **1.4 Composition of Functions and Invertible Function**

**Definition 8** Let *f* : A → B and *g* : B → C be two functions. Then the composition of *f* and *g*, denoted by *gof*, is defined as the function *gof* : A → C given by

$$g o f(x)=g(f(x)),\ \forall\ x\in\mathrm{A}.$$

![](_page_11_Figure_4.jpeg)

$$\mathrm{Fig\,1.5}$$

**Example 15** Let *f* : {2, 3, 4, 5} → {3, 4, 5, 9} and *g* : {3, 4, 5, 9} → {7, 11, 15} be functions defined as *f*(2) = 3, *f*(3) = 4, *f*(4) = *f*(5) = 5 and *g* (3) = *g* (4) = 7 and *g* (5) = *g* (9) = 11. Find *gof*.

**Solution** We have *gof*(2) = *g* (*f*(2)) = *g* (3) = 7, *gof* (3) = *g* (*f*(3)) = *g* (4) = 7, *gof*(4) = *g* (*f*(4)) = *g* (5) = 11 and *gof*(5) = *g* (5) = 11.

**Example 16** Find *gof* and *fog*, if *f* : **R** → **R** and *g* : **R** → **R** are given by *f*(*x*) = cos *x* and *g* (*x*) = 3*x* 2 . Show that *gof* ≠ *fog*.

**Solution** We have *gof*(*x*) = *g* (*f*(*x*)) = *g* (cos *x*) = 3 (cos *x*) 2 = 3 cos2 *x*. Similarly, *fog*(*x*) = *f*(*g* (*x*)) = *f*(3*x* 2 ) = cos (3*x* 2 ). Note that 3cos2 *x* ≠ cos 3*x* 2 , for *x* = 0. Hence, *gof* ≠ *fog*.

**Definition 9** A function *f* : X → Y is defined to be *invertible*, if there exists a function *g* : Y → X such that *gof* = IX and *fog* = IY . The function *g* is called the *inverse of f* and is denoted by *f* –1 .

Thus, if *f* is invertible, then *f* must be one-one and onto and conversely, if *f* is one-one and onto, then *f* must be invertible. This fact significantly helps for proving a function *f* to be invertible by showing that *f* is one-one and onto, specially when the actual inverse of *f* is not to be determined.

**Example 17** Let *f* : **N** → Y be a function defined as *f*(*x*) = 4*x* + 3, where, Y = {*y* ∈ **N**: *y* = 4*x* + 3 for some *x* ∈ **N**}. Show that *f* is invertible. Find the inverse.

**Solution** Consider an arbitrary element *y* of Y. By the definition of Y, *y* = 4*x* + 3,

for some *x* in the domain **N**. This shows that ( 3) 4 *y x* − = . Define *g* : Y → **N** by

$g(y)=\frac{(y-3)}{4}$. Now, $gof(x)=g(f(x))=g(4x+3)=\frac{(4x+3-3)}{4}=x$ and 

*fog* (*y*) = *f*(*g* (*y*)) = *f* ( 3) 4 ( 3) 3 4 4 *y y* − − = + = *y* – 3 + 3 = *y*. This shows that *gof* = IN

and *fog* = IY , which implies that *f* is invertible and *g* is the inverse of *f*.

## *Miscellaneous Examples*

**Example 18** If R1 and R2 are equivalence relations in a set A, show that R1 ∩ R2 is also an equivalence relation.

**Solution** Since R1 and R2 are equivalence relations, (*a*, *a*) ∈ R1 , and (*a*, *a*) ∈ R2 ∀ *a* ∈A. This implies that (*a*, *a*) ∈ R1 ∩ R2 , ∀ *a*, showing R1 ∩ R2 is reflexive. Further, (*a*, *b*) ∈ R1 ∩ R2 ⇒ (*a*, *b*) ∈ R1 and (*a*, *b*) ∈ R2 ⇒ (*b*, *a*) ∈ R1 and (*b*, *a*) ∈ R2 ⇒ (*b*, *a*) ∈ R1 ∩ R2 , hence, R1 ∩ R2 is symmetric. Similarly, (*a*, *b*) ∈ R1 ∩ R2 and (*b*, *c*) ∈ R1 ∩ R2 ⇒ (*a*, *c*) ∈ R1 and (*a*, *c*) ∈ R2 ⇒ (*a*, *c*) ∈ R1 ∩ R2 . This shows that R1 ∩ R2 is transitive. Thus, R1 ∩ R2 is an equivalence relation.

**Example 19** Let R be a relation on the set A of ordered pairs of positive integers defined by (*x*, *y*) R (*u*, *v*) if and only if *xv* = *yu*. Show that R is an equivalence relation.

**Solution** Clearly, (*x*, *y*) R (*x*, *y*), ∀ (*x*, *y*) ∈ A, since *xy* = *yx*. This shows that R is reflexive. Further, (*x*, *y*) R (*u*, *v*) ⇒ *xv* = *yu* ⇒ *uy* = *vx* and hence (*u*, *v*) R (*x*, *y*). This shows that R is symmetric. Similarly, (*x*, *y*) R (*u*, *v*) and (*u*, *v*) R (*a*, *b*) ⇒ *xv* = *yu* and

$ub=va\Rightarrow\ xy\ \frac{a}{u}=yu\ \frac{a}{u}\Rightarrow\ xy\ \frac{b}{v}=yu\ \frac{a}{u}\Rightarrow\ xb=ya$ and hence $(x,y)\ R\ (a,b)$. Thus, $R$ is transitive. Thus $R$ is $\infty$-eliminate solution.  
  

is transitive. Thus, R is an equivalence relation.

**Example 20** Let X = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Let R1 be a relation in X given by R1 = {(*x*, *y*) : *x* – *y* is divisible by 3} and R2 be another relation on X given by R2 = {(*x*, *y*): {*x*, *y*} ⊂ {1, 4, 7}} or {*x*, *y*} ⊂ {2, 5, 8} or {*x*, *y*} ⊂ {3, 6, 9}}. Show that R1 = R2 .

**Solution** Note that the characteristic of sets {1, 4, 7}, {2, 5, 8} and {3, 6, 9} is that difference between any two elements of these sets is a multiple of 3. Therefore, (*x*, *y*) ∈ R1 ⇒ *x* – *y* is a multiple of 3 ⇒ {*x*, *y*} ⊂ {1, 4, 7} or {*x*, *y*} ⊂ {2, 5, 8} or {*x*, *y*} ⊂ {3, 6, 9} ⇒ (*x*, *y*) ∈ R2 . Hence, R1 ⊂ R2 . Similarly, {*x*, *y*} ∈ R2 ⇒ {*x*, *y*}

⊂ {1, 4, 7} or {*x*, *y*} ⊂ {2, 5, 8} or {*x*, *y*} ⊂ {3, 6, 9} ⇒ *x* – *y* is divisible by 3 ⇒ {*x*, *y*} ∈ R1 . This shows that R2 ⊂ R1 . Hence, R1 = R2 .

**Example 21** Let *f* : X → Y be a function. Define a relation R in X given by R = {(*a*, *b*): *f*(*a*) = *f*(*b*)}. Examine whether R is an equivalence relation or not.

**Solution** For every *a* ∈ X, (*a*, *a*) ∈ R, since *f*(*a*) = *f*(*a*), showing that R is reflexive. Similarly, (*a*, *b*) ∈ R ⇒ *f*(*a*) = *f*(*b*) ⇒ *f*(*b*) = *f*(*a*) ⇒ (*b*, *a*) ∈ R. Therefore, R is symmetric. Further, (*a*, *b*) ∈ R and (*b*, *c*) ∈ R ⇒ *f*(*a*) = *f*(*b*) and *f*(*b*) = *f*(*c*) ⇒ *f*(*a*) = *f*(*c*) ⇒ (*a*, *c*) ∈ R, which implies that R is transitive. Hence, R is an equivalence relation.

**Example 22** Find the number of all one-one functions from set A = {1, 2, 3} to itself.

**Solution** One-one function from {1, 2, 3} to itself is simply a permutation on three symbols 1, 2, 3. Therefore, total number of one-one maps from {1, 2, 3} to itself is same as total number of permutations on three symbols 1, 2, 3 which is 3! = 6.

**Example 23** Let A = {1, 2, 3}. Then show that the number of relations containing (1, 2) and (2, 3) which are reflexive and transitive but not symmetric is three.

**Solution** The smallest relation R1 containing (1, 2) and (2, 3) which is reflexive and transitive but not symmetric is {(1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (1, 3)}. Now, if we add the pair (2, 1) to R1 to get R2 , then the relation R2 will be reflexive, transitive but not symmetric. Similarly, we can obtain R3 by adding (3, 2) to R1 to get the desired relation. However, we can not add two pairs (2, 1), (3, 2) or single pair (3, 1) to R1 at a time, as by doing so, we will be forced to add the remaining pair in order to maintain transitivity and in the process, the relation will become symmetric also which is not required. Thus, the total number of desired relations is three.

**Example 24** Show that the number of equivalence relation in the set {1, 2, 3} containing (1, 2) and (2, 1) is two.

**Solution** The smallest equivalence relation R1 containing (1, 2) and (2, 1) is {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}. Now we are left with only 4 pairs namely (2, 3), (3, 2), (1, 3) and (3, 1). If we add any one, say (2, 3) to R1 , then for symmetry we must add (3, 2) also and now for transitivity we are forced to add (1, 3) and (3, 1). Thus, the only equivalence relation bigger than R1 is the universal relation. This shows that the total number of equivalence relations containing (1, 2) and (2, 1) is two.

**Example 25** Consider the identity function I **N** : **N** → **N** defined as I **N** (*x*) = *x* ∀ *x* ∈ **N**. Show that although I**N** is onto but I**N** + I**N** : **N** → **N** defined as

$\left(\mathrm{I}_{\mathrm{N}}+\mathrm{I}_{\mathrm{N}}\right)\left(x\right)=\mathrm{I}_{\mathrm{N}}\left(x\right)+\mathrm{I}_{\mathrm{N}}\left(x\right)=x+x=2x$ is not onto.  
  

**Solution** Clearly I**N** is onto. But I**N** + I**N** is not onto, as we can find an element 3 in the co-domain **N** such that there does not exist any *x* in the domain **N** with (I**N** + I**N** ) (*x*) = 2*x* = 3.

**Example 26** Consider a function *f* : 0, 2 π → **R** given by *f*(*x*) = sin *x* and

*g* : 0, 2 π → **R** given by *g*(*x*) = cos *x*. Show that *f* and *g* are one-one, but *f* + *g* is not

one-one.

**Solution** Since for any two distinct elements *x*1 and *x*2 in 0, 2 π , sin *x*1 ≠ sin *x*2 and cos *x*1 ≠ cos *x*2 , both *f* and *g* must be one-one. But (*f* + *g*) (0) = sin 0 + cos 0 = 1 and (*f* + *g*) 2 π = sin cos 1 2 2 π π + = . Therefore, *f* + *g* is not one-one.

## *Miscellaneous Exercise on Chapter 1*

- **1.** Show that the function *f* : **R** → {*x* ∈ **R** : 1 < *x* < 1} defined by ( ) 1 | | *x f x x* = + , *x* ∈ **R** is one one and onto function.
**2.** Show that the function *f* : **R** → **R** given by *f*(*x*) = *x* 3 is injective.

- **3.** Given a non empty set X, consider P(X) which is the set of all subsets of X. Define the relation R in P(X) as follows: For subsets A, B in P(X), ARB if and only if A ⊂ B. Is R an equivalence relation on P(X)? Justify your answer.
- **4.** Find the number of all onto functions from the set {1, 2, 3,......, *n*} to itself.
- **5.** Let A = {– 1, 0, 1, 2}, B = {– 4, 2, 0, 2} and *f*, *g* : A → B be functions defined 1

by *f*(*x*) = *x* 2 – *x*, *x* ∈ A and ( ) 2 1, 2 *g x x* = − − *x* ∈ A. Are *f* and *g* equal? Justify your answer. (Hint: One may note that two functions *f* : A → B and *g* : A → B such that *f*(*a*) = *g*(*a*) ∀ *a* ∈ A, are called equal functions).

- **6.** Let A = {1, 2, 3}. Then number of relations containing (1, 2) and (1, 3) which are reflexive and symmetric but not transitive is
- (A) 1 (B) 2 (C) 3 (D) 4 **7.** Let A = {1, 2, 3}. Then number of equivalence relations containing (1, 2) is
	- (A) 1 (B) 2 (C) 3 (D) 4

## *Summary*

In this chapter, we studied different types of relations and equivalence relation, composition of functions, invertible functions and binary operations. The main features of this chapter are as follows:

- Æ *Empty relation* is the relation R in X given by R = φ ⊂ X × X.
- Æ *Universal relation* is the relation R in X given by R = X × X.
- Æ *Reflexive relation* R in X is a relation with (*a*, *a*) ∈ R ∀ *a* ∈ X.
- Æ *Symmetric relation* R in X is a relation satisfying (*a*, *b*) ∈ R implies (*b*, *a*) ∈ R.
- Æ *Transitive relation* R in X is a relation satisfying (*a*, *b*) ∈ R and (*b*, *c*) ∈ R implies that (*a*, *c*) ∈ R.
- Æ *Equivalence relation* R in X is a relation which is reflexive, symmetric and transitive.
- Æ *Equivalence class* [*a*] containing *a* ∈ X for an equivalence relation R in X is the subset of X containing all elements *b* related to *a*.
- Æ A function *f* : X → Y is *one-one* (or *injective*) if

*f*(*x*1 ) = *f*(*x*2 ) ⇒ *x*1 = *x*2 ∀ *x*1 , *x*2 ∈ X.

- Æ A function *f* : X → Y is *onto* (or *surjective*) if given any *y* ∈ Y, ∃ *x* ∈ X such that *f*(*x*) = *y*.
- Æ A function *f* : X → Y is *one-one and onto* (or *bijective*), if *f* is both one-one and onto.
- Æ Given a finite set X, a function *f* : X → X is one-one (respectively onto) if and only if *f* is onto (respectively one-one). This is the characteristic property of a finite set. This is not true for infinite set

## *Historical Note*

The concept of function has evolved over a long period of time starting from R. Descartes (1596-1650), who used the word 'function' in his manuscript "*Geometrie*" in 1637 to mean some positive integral power *x n* of a variable *x* while studying geometrical curves like hyperbola, parabola and ellipse. James Gregory (1636-1675) in his work " *Vera Circuli et Hyperbolae Quadratura*" (1667) considered function as a quantity obtained from other quantities by successive use of algebraic operations or by any other operations. Later G. W. Leibnitz (1646-1716) in his manuscript "*Methodus tangentium inversa, seu de functionibus*" written in 1673 used the word 'function' to mean a quantity varying from point to point on a curve such as the coordinates of a point on the curve, the slope of the curve, the tangent and the normal to the curve at a point. However, in his manuscript "*Historia*" (1714), Leibnitz used the word 'function' to mean quantities that depend on a variable. He was the first to use the phrase 'function of *x*'. John Bernoulli (1667-1748) used the notation φ*x* for the first time in 1718 to indicate a function of *x*. But the general adoption of symbols like *f*, F, φ, ψ ... to represent functions was made by Leonhard Euler (1707-1783) in 1734 in the first part of his manuscript "*Analysis Infinitorium*". Later on, Joeph Louis Lagrange (1736-1813) published his manuscripts "*Theorie des functions analytiques*" in 1793, where he discussed about analytic function and used the notion *f* (*x*), F(*x*), φ(*x*) etc. for different function of *x*. Subsequently, Lejeunne Dirichlet (1805-1859) gave the definition of function which was being used till the set theoretic definition of function presently used, was given after set theory was developed by Georg Cantor (1845-1918). The set theoretic definition of function known to us presently is simply an abstraction of the definition given by Dirichlet in a rigorous manner.

**—**v**—**

