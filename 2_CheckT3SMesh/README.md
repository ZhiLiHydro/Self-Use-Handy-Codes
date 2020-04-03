### 2_Check T3S Mesh: Why my mesh gives me bad results?

#### To run:

```
python checkt3smesh.py
```

This code is to visualize the quality of a T3S format finite element mesh. T3S format mesh file is essential for numerical modeling using [TELEMAC](http://www.opentelemac.org/).

#### Prerequisites

* Python >= 3.5
* Numpy+Scipy+Matplotlib
* Numba ([nopython=True](https://numba.pydata.org/numba-doc/latest/user/5minguide.html) is on by default)

#### Example:

Enter the file name `example.t3s`. Result would be like this:

![intro](https://github.com/ZhiLiHydro/Self-Use-Handy-Codes/blob/master/2_CheckT3SMesh/example.png)

#### To do

- [ ] Add a handle on boundary elements

