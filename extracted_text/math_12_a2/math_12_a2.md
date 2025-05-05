![](_page_0_Picture_0.jpeg)

# **A.2.1 Introduction**

196 MATHEMATICS

In class XI, we have learnt about mathematical modelling as an attempt to study some part (or form) of some real-life problems in mathematical terms, i.e., the conversion of a physical situation into mathematics using some suitable conditions. Roughly speaking mathematical modelling is an activity in which we make models to describe the behaviour of various phenomenal activities of our interest in many ways using words, drawings or sketches, computer programs, mathematical formulae etc.

In earlier classes, we have observed that solutions to many problems, involving applications of various mathematical concepts, involve mathematical modelling in one way or the other. Therefore, it is important to study mathematical modelling as a separate topic.

In this chapter, we shall further study mathematical modelling of some real-life problems using techniques/results from matrix, calculus and linear programming.

# **A.2.2 Why Mathematical Modelling?**

Students are aware of the solution of word problems in arithmetic, algebra, trigonometry and linear programming etc. Sometimes we solve the problems without going into the physical insight of the situational problems. Situational problems need physical insight that is **introduction** of physical laws and some symbols to compare the mathematical results obtained with practical values. To solve many problems faced by us, we need a technique and this is what is known as *mathematical modelling.* Let us consider the following problems:

- (i) To find the width of a river (particularly, when it is difficult to cross the river).
- (ii) To find the optimal angle in case of shot-put (by considering the variables such as : the height of the thrower, resistance of the media, acceleration due to gravity etc.).
- (iii) To find the height of a tower (particularly, when it is not possible to reach the top of the tower).
- (iv) To find the temperature at the surface of the Sun.
- (v) Why heart patients are not allowed to use lift? (without knowing the physiology of a human being).
- (vi) To find the mass of the Earth.
- (vii) Estimate the yield of pulses in India from the standing crops (a person is not allowed to cut all of it).
- (viii) Find the volume of blood inside the body of a person (a person is not allowed to bleed completely).
- (ix) Estimate the population of India in the year 2020 (a person is not allowed to wait till then).

All of these problems can be solved and infact have been solved with the help of Mathematics using mathematical modelling. In fact, you might have studied the methods for solving some of them in the present textbook itself. However, it will be instructive if you first try to solve them yourself and that too without the help of Mathematics, if possible, you will then appreciate the power of Mathematics and the need for mathematical modelling.

## **A.2.3 Principles of Mathematical Modelling**

Mathematical modelling is a principled activity and so it has some principles behind it. These principles are almost philosophical in nature. Some of the basic principles of mathematical modelling are listed below in terms of instructions:

- (i) Identify the need for the model. (for what we are looking for)
- (ii) List the parameters/variables which are required for the model.
- (iii) Identify the available relevent data. (what is given?)
- (iv) Identify the circumstances that can be applied (assumptions)
- (v) Identify the governing physical principles.
- (vi) Identify
	- (a) the equations that will be used.
	- (b) the calculations that will be made.
	- (c) the solution which will follow.
- (vii) Identify tests that can check the
	- (a) consistency of the model.
	- (b) utility of the model.
- (viii) Identify the parameter values that can improve the model.

The above principles of mathematical modelling lead to the following: steps for mathematical modelling.

- **Step 1:** Identify the physical situation.
- **Step 2:** Convert the physical situation into a mathematical model by introducing parameters / variables and using various known physical laws and symbols.
- **Step 3:** Find the solution of the mathematical problem.
- **Step 4:** Interpret the result in terms of the original problem and compare the result with observations or experiments.
- **Step 5:** If the result is in good agreement, then accept the model. Otherwise modify the hypotheses / assumptions according to the physical situation and go to Step 2.

The above steps can also be viewed through the following diagram:

![](_page_2_Figure_8.jpeg)

**Example 1** Find the height of a given tower using mathematical modelling.

**Solution Step 1** Given physical situation is "to find the height of a given tower". **Step 2** Let AB be the given tower (Fig A.2.2). Let PQ be an observer measuring the height of the tower with his eye at P. Let PQ = *h* and let height of tower be H. Let α be the angle of elevation from the eye of the observer to the top of the tower.

![](_page_2_Figure_11.jpeg)

Let 
$$l=\text{PC}=\text{QB}$$
. 

Now  
  

$$\tan\alpha=\frac{\text{AC}}{\text{PC}}=\frac{\text{H}-h}{l}$$

or H = *h* + *l* tan α ... (1)

**Step 3** Note that the values of the parameters *h*, *l* and α (using sextant) are known to the observer and so (1) gives the solution of the problem.

**Step 4** In case, if the foot of the tower is not accessible, i.e., when *l* is not known to the observer, let β be the angle of depression from P to the foot B of the tower. So from ∆PQB, we have

$$\tan\beta={\frac{\mathrm{PQ}}{\mathrm{QB}}}={\frac{h}{l}}{\mathrm{~or~}}l=h{\mathrm{~cot~}}\beta$$

**Step 5** is not required in this situation as exact values of the parameters *h*, *l*, α and β are known.

**Example 2** Let a business firm produces three types of products P1 , P2 and P3 that uses three types of raw materials R1 , R2 and R3 . Let the firm has purchase orders from two clients F1 and F2 . Considering the situation that the firm has a limited quantity of R1 , R2 and R3 , respectively, prepare a model to determine the quantities of the raw material R1 , R2 and R3 required to meet the purchase orders.

**Solution Step 1** The physical situation is well identified in the problem.

**Step 2** Let A be a matrix that represents purchase orders from the two clients F1 and F2 . Then, A is of the form

$$\mathbf{A}={\begin{array}{l l l}{\mathbf{P}_{1}}&{\mathbf{P}_{2}}&{\mathbf{P}_{3}}\\ {\mathbf{F}_{1}\left[\bullet\ \bullet\ \bullet\ \bullet\ \bullet\right]}\\ {\mathbf{F}_{2}\left[\bullet\ \bullet\ \bullet\ \bullet\right]}\end{array}}$$

Let B be the matrix that represents the amount of raw materials R1 , R2 and R3 , required to manufacture each unit of the products P1 , P2 and P3 . Then, B is of the form

$$\begin{array}{c}{{\mathrm{R}_{1}\,\mathrm{R}_{2}\,\mathrm{R}_{3}}}\\ {{\mathrm{P}_{1}\left[\bullet\,\,\bullet\,\,\bullet\right]}}\\ {{\mathrm{B}=\mathrm{P}_{2}}}\\ {{\mathrm{P}_{3}\left[\bullet\,\,\bullet\,\,\bullet\right]}}\end{array}$$

**Step 3** Note that the product (which in this case is well defined) of matrices A and B is given by the following matrix

1 2 3 1 2 R R R F • • • AB F • • • =

which in fact gives the desired quantities of the raw materials R1 , R2 and R3 to fulfill the purchase orders of the two clients F1 and F2 .

**Example 3** Interpret the model in Example 2, in case

$$\mathbf{A}={\left[\begin{array}{l l l}{10}&{15}&{6}\\ {10}&{20}&{0}\end{array}\right]},\ \mathbf{B}={\left[\begin{array}{l l l}{3}&{4}&{0}\\ {7}&{9}&{3}\\ {5}&{12}&{7}\end{array}\right]}$$

and the available raw materials are 330 units of R1 , 455 units of R2 and 140 units of R3 . **Solution** Note that

AB = 3 4 0 10 15 6 7 9 3 10 20 0 5 12 7 = R R R F F 1 2 3 1 2 165 247 87 170 220 60 

This clearly shows that to meet the purchase order of F1 and F2 , the raw material required is 335 units of R1 , 467 units of R2 and 147 units of R3 which is much more than the available raw material. Since the amount of raw material required to manufacture each unit of the three products is fixed, we can either ask for an increase in the available raw material or we may ask the clients to reduce their orders.

*Remark* If we replace A in Example 3 by A1 given by

$$\mathbf{A}_{1}={\left[\begin{array}{l l l}{9}&{12}&{6}\\ {10}&{20}&{0}\end{array}\right]}$$

i.e., if the clients agree to reduce their purchase orders, then

$\mathbf{A}_{1}\,\mathbf{B}=\begin{bmatrix}9&12&6\\ 10&20&0\end{bmatrix}\begin{bmatrix}3&4&0\\ 7&9&3\\ 5&12&7\end{bmatrix}=\begin{bmatrix}141&216&78\\ 170&220&60\end{bmatrix}$

This requires 311 units of R1 , 436 units of R2 and 138 units of R3 which are well below the available raw materials, i.e., 330 units of R1 , 455 units of R2 and 140 units of R3 . Thus, if the revised purchase orders of the clients are given by A1 , then the firm can easily supply the purchase orders of the two clients.

A**Note** One may further modify A so as to make full use of the available raw material.

**Query** Can we make a mathematical model with a given B and with fixed quantities of the available raw material that can help the firm owner to ask the clients to modify their orders in such a way that the firm makes the full use of its available raw material?

The answer to this query is given in the following example:

**Example 4** Suppose P1 , P2 , P3 and R1 , R2 , R3 are as in Example 2. Let the firm has 330 units of R1 , 455 units of R2 and 140 units of R3 available with it and let the amount of raw materials R1 , R2 and R3 required to manufacture each unit of the three products is given by

  
  
**Acknowledgement**  
  
I would like to thank my supervisor, for his kind of support. I would like to thank my supervisor, for his kind of support.  
  

How many units of each product is to be made so as to utilise the full available raw material?

**Solution Step 1** The situation is easily identifiable.

**Step 2** Suppose the firm produces *x* units of P1 , *y* units of P2 and *z* units of P3 . Since product P1 requires 3 units of R1 , P2 requires 7 units of R1 and P3 requires 5 units of R1 (observe matrix B) and the total number of units, of R1 , available is 330, we have

> 3*x* + 7*y* + 5*z* = 330 (for raw material R1 )

Similarly, we have

$4x+9y+12z=455$ (for raw material R${}_{2}$)  
  
$3y+7z=140$ (for raw material R${}_{3}$)

This system of equations can be expressed in matrix form as

|   |  |  |  |
| --- | --- | --- | --- |
| 0 |  | 4 | 3 |
| 3 |  | 9 | 7 |
| 7 |  | 12 | 5 |
|   |  |  |  |
|   |  |  |  |
| z | y |  | x |
|   |  |  |  |
|  |  | = |  |
|   |  |  |  |
| 140 |  | 455 | 330 |
|   |  |  |  |

**Step 3** Using elementary row operations, we obtain

$${\left[\begin{array}{l l l}{1}&{0}&{0}\\ {0}&{1}&{0}\\ {0}&{0}&{1}\end{array}\right]}{\left[\begin{array}{l}{x}\\ {y}\\ {z}\end{array}\right]}={\left[\begin{array}{l}{20}\\ {35}\\ {5}\end{array}\right]}$$

This gives *x* = 20, *y* = 35 and *z* = 5. Thus, the firm can produce 20 units of P1 , 35 units of P2 and 5 units of P3 to make full use of its available raw material.

*Remark* One may observe that if the manufacturer decides to manufacture according to the available raw material and not according to the purchase orders of the two clients F1 and F2 (as in Example 3), he/she is unable to meet these purchase orders as F1 demanded 6 units of P3 where as the manufacturer can make only 5 units of P3 .

**Example 5** A manufacturer of medicines is preparing a production plan of medicines M1 and M2 . There are sufficient raw materials available to make 20000 bottles of M1 and 40000 bottles of M2 , but there are only 45000 bottles into which either of the medicines can be put. Further, it takes 3 hours to prepare enough material to fill 1000 bottles of M1 , it takes 1 hour to prepare enough material to fill 1000 bottles of M2 and there are 66 hours available for this operation. The profit is Rs 8 per bottle for M1 and Rs 7 per bottle for M2 . How should the manufacturer schedule his/her production in order to maximise profit?

**Solution Step 1** To find the number of bottles of M1 and M2 in order to maximise the profit under the given hypotheses.

**Step 2** Let *x* be the number of bottles of type M1 medicine and *y* be the number of bottles of type M2 medicine. Since profit is Rs 8 per bottle for M1 and Rs 7 per bottle for M2 , therefore the objective function (which is to be maximised) is given by

$$Z=Z\left(x,y\right)=8x+7y$$

The objective function is to be maximised subject to the constraints (Refer Chapter 12 on Linear Programming)

$$\left.\begin{array}{l}x\leq20000\\ y\leq40000\\ x+y\leq45000\\ 3x+y\leq66000\\ x\geq0,y\geq0\end{array}\right\}\tag{1}$$

**Step 3** The shaded region OPQRST is the feasible region for the constraints (1) (Fig A.2.3). The co-ordinates of vertices O, P, Q, R, S and T are (0, 0), (20000, 0), (20000, 6000), (10500, 34500), (5000, 40000) and (0, 40000), respectively.

![](_page_7_Figure_1.jpeg)

**Fig A.2.3**

Note that

Z at P (0, 0) = 0 Z at P (20000, 0) = 8 × 20000 = 160000 Z at Q (20000, 6000) = 8 × 20000 + 7 × 6000 = 202000 Z at R (10500, 34500) = 8 × 10500 + 7 × 34500 = 325500 Z at S = (5000, 40000) = 8 × 5000 + 7 × 40000 = 320000 Z at T = (0, 40000) = 7 × 40000 = 280000

Now observe that the profit is maximum at *x* = 10500 and *y* = 34500 and the maximum profit is `325500. Hence, the manufacturer should produce 10500 bottles of M1 medicine and 34500 bottles of M2 medicine in order to get maximum profit of `325500.

**Example 6** Suppose a company plans to produce a new product that incur some costs (fixed and variable) and let the company plans to sell the product at a fixed price. Prepare a mathematical model to examine the profitability.

**Solution Step 1** Situation is clearly identifiable.

**Step 2 Formulation:** We are given that the costs are of two types: fixed and variable. The fixed costs are independent of the number of units produced (e.g., rent and rates), while the variable costs increase with the number of units produced (e.g., material). Initially, we assume that the variable costs are directly proportional to the number of units produced — this should simplify our model. The company earn a certain amount of money by selling its products and wants to ensure that it is maximum. For convenience, we assume that all units produced are sold immediately.

## **The mathematical model**

- Let *x* = number of units produced and sold
	- C = total cost of production (in rupees)
	- I = income from sales (in rupees)

P = profit (in rupees)

Our assumptions above state that C consists of two parts:

(i) fixed cost = *a* (in rupees),

(ii) variable cost = $b$ (rupees/unit produced). Then  
  

$$C=a\neq bx^{\flat}$$
...\tag{1}

Also, income I depends on selling price *s* (rupees/unit)

Thus I = *sx* ... (2)

The profit P is then the difference between income and costs. So

$$\begin{array}{l}\mbox{P}=\mbox{I}-\mbox{C}\\ \mbox{}=\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{}}}}}}}}}}}}}}}\mbox{}(a+bx)\\ \mbox{}=\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{\mbox{}}}}}}}}}}}}}}\mbox{}(s-b)\mbox{x-a}\end{array}\tag{3}$$

*We now have a mathematical model of the relationships* (1) to (3) *between the variables x,* C, I, P*, a, b, s.* These variables may be classified as:

| independent | x |
| --- | --- |
| dependent | C, I, P |
| parameters | a, b, s |

The manufacturer, knowing *x*, *a*, *b*, *s* can determine P.

**Step 3** From (3), we can observe that for the break even point (i.e., make neither profit

nor loss), he must have P = 0, i.e., units. *a x s b* = −

**Steps 4 and 5** In view of the break even point, one may conclude that if the company

produces few units, i.e., less than units *a x s b* = − , then the company will suffer loss and if it produces large number of units, i.e., much more than units *a s b* − , then it can

make huge profit. Further, if the break even point proves to be unrealistic, then another model could be tried or the assumptions regarding cash flow may be modified.

*Remark* From (3), we also have

$${\frac{d\,\mathbf{P}}{d\,x}}=s-b$$

This means that rate of change of P with respect to *x* depends on the quantity *s* – *b*, which is the difference of selling price and the variable cost of each product. Thus, in order to gain profit, this should be positive and to get large gains, we need to produce large quantity of the product and at the same time try to reduce the variable cost.

**Example 7** Let a tank contains 1000 litres of brine which contains 250 g of salt per litre. Brine containing 200 g of salt per litre flows into the tank at the rate of 25 litres per minute and the mixture flows out at the same rate. Assume that the mixture is kept uniform all the time by stirring. What would be the amount of salt in the tank at any time *t*?

**Solution Step 1** The situation is easily identifiable.

**Step 2** Let *y* = *y* (*t*) denote the amount of salt (in kg) in the tank at time *t* (in minutes) after the inflow, outflow starts. Further assume that *y* is a differentiable function. When *t* = 0, i.e., before the inflow–outflow of the brine starts,

* [16] A. A. K. K.  
  

Note that the change in *y* occurs due to the inflow, outflow of the mixture.

Now the inflow of brine brings salt into the tank at the rate of 5 kg per minute (as 25 × 200 g = 5 kg) and the outflow of brine takes salt out of the tank at the rate of

$25\left(\frac{y}{1000}\right)$= $\frac{y}{40}$ kg per minute (as at time $t$, the salt in the tank is $\frac{y}{1000}$ kg).  
  

Thus, the rate of change of salt with respect to *t* is given by

$$\frac{dy}{dt}=5-\frac{y}{40}$$
 (Why?) 
$$\frac{dy}{dt}+\frac{1}{40}y=5$$
... (1)

or

This gives a mathematical model for the given problem.

**Step 3** Equation (1) is a linear equation and can be easily solved. The solution of (1) is given by

> *t e* −

40 *t e* −

$$ye^{\frac{t}{40}}=200e^{\frac{t}{40}}+C\ \mbox{or}\ y\ (t)=200+C\ e^{-\frac{t}{40}}\qquad\qquad...\tag{2}$$

... (3)

where, *c* is the constant of integration.

Note that when *t* = 0, *y* = 250. Therefore, 250 = 200 + C or C = 50

*y* = 200 + 50 40

=

50 *y* −200

200 50 *y* −

40 *t e* =

Then (2) reduces to

or

or

Therefore  
  

$$t=\frac{40\log_{e}\left(\frac{50}{y-200}\right)}{\left(\frac{50}{y-200}\right)}\tag{4}$$

Here, the equation (4) gives the time *t* at which the salt in tank is *y* kg.

**Step 4** Since 40 *t e* − is always positive, from (3), we conclude that *y* > 200 at all times Thus, the minimum amount of salt content in the tank is 200 kg.

Also, from (4), we conclude that *t* > 0 if and only if 0 < *y* – 200 < 50 i.e., if and only if 200 < *y* < 250 i.e., the amount of salt content in the tank after the start of inflow and outflow of the brine is between 200 kg and 250 kg.

## *Limitations of Mathematical Modelling*

Till today many mathematical models have been developed and applied successfully to understand and get an insight into thousands of situations. Some of the subjects like mathematical physics, mathematical economics, operations research, bio-mathematics etc. are almost synonymous with mathematical modelling.

But there are still a large number of situations which are yet to be modelled. The reason behind this is that either the situation are found to be very complex or the mathematical models formed are mathematically intractable.

The development of the powerful computers and super computers has enabled us to mathematically model a large number of situations (even complex situations). Due to these fast and advanced computers, it has been possible to prepare more realistic models which can obtain better agreements with observations.

However, we do not have good guidelines for choosing various parameters / variables and also for estimating the values of these parameters / variables used in a mathematical model. Infact, we can prepare reasonably accurate models to fit any data by choosing five or six parameters / variables. We require a minimal number of parameters / variables to be able to estimate them accurately.

Mathematical modelling of large or complex situations has its own special problems. These type of situations usually occur in the study of world models of environment, oceanography, pollution control etc. Mathematical modellers from all disciplines mathematics, computer science, physics, engineering, social sciences, etc., are involved in meeting these challenges with courage.

**—**v**—**

