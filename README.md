# twopiece: Two Piece Distributions

- **Homepage:** https://github.com/quantgirluk/tpdist/tree/master/twopiece
- **Free software:** MIT license


### Overview

The **twopiece** library provides a Python implementation of the family of Two Piece distributions. 

The family of univariate two–piece distributions is a family of univariate three-parameter location-scale models, where skewness is introduced 
by differing scale parameters either side of the location. For details on this family of distributions we refer to 
[Inference in Two-Piece Location-Scale Models with Jeffreys Priors](https://projecteuclid.org/euclid.ba/1393251764)
published in Bayesian Anal.
Volume 9, Number 1 (2014), 1-22 and the references therein.


### Supported Distributions
Implementation is provided for the following distributions

#### Three Parameters

- two-piece normal [[+ info]](https://en.wikipedia.org/wiki/Split_normal_distribution)
- two-piece Laplace
- two-piece Cauchy
- two-piece logistic

#### Four Parameters

- two-piece t
- two-piece exponential power


### Main Features
We provide the following functionality:

- probability density function ***pdf***
- cumulative distribution function ***cdf***
- quantile function ***ppf***
- random generation ***random_sample***

for all the supported distributions.


### Quick Start

To illustrate usage of the features for the 3 and 4 parameters distributions we will use 
the two-piece normal, and two-piece t, respectively. The behaviour is analogous for the rest of the supported distributions.


#### 1. Create a twopiece instance
To create an instance we need to specify either 3 or 4 parameters:

For the **two-piece normal** we require:

- *loc*: which is the location parameter
- *sigma1*, *sigma2* : which are both scale parameters
 
```
loc=0.0
sigma1=1.0
sigma2=1.0
dist = tpnorm(loc=loc, sigma1=sigma1, sigma2=sigma2)
```

For the **two-piece t** we require:

- *loc*: which is the location parameter
- *sigma1*, *sigma2* : which are both scale parameters
- *shape* : which defines the degrees of freedom for the t-Student distribution
 
```
loc=0.0
sigma1=1.0
sigma2=1.0
shape=3.0
dist = tpstudent(loc=loc, sigma1=sigma1, sigma2=sigma2, shape=shape)
```

Hereafter we assume that there is a twopiece instance called *dist*.

#### 2. Evaluate and visualise the probability density function (pdf)
We can evaluate the pdf on a single point or an array type object

```
dist.pdf(0)
```

```
dist.pdf([0.0,0.25,0.5])
```

To visualise the pdf use
```
x = arange(-12, 12, 0.1)
y = dist.pdf(x)
plt.plot(x, y)
```

#### 3. Evaluate the cumulative distribution function (cdf)
We can evaluate the cdf on a single point or an array type object
```
dist.cdf(0)
```

```
dist.cdf([0.0,0.25,0.5])
```

To visualise the cdf use

```
x = arange(-12, 12, 0.1)
y = dist.cdf(x)
plt.plot(x, y)
```

#### 4. Evaluate the quantile function (ppf)
We can evaluate the ppf on a single point or an array type object. Note that the ppf has support on [0,1].
```
dist.ppf(0.95)
```

```
dist.ppf([0.5, 0.9, 0.95])
```

To visualise the ppf use
```
x = arange(0.001, 0.999, 0.01)
y = dist.ppf(x)
plt.plot(x, y)
```

#### 5. Generate a random sample

To generate a random sample we require: 
- *size*: which is simply the size of the sample

```
sample = dist.random_sample(size = 100)
```

### Install

#### Requirements

**twopiece** has been developed and tested on [Python 3.6, and 3.7](https://www.python.org/downloads/)




