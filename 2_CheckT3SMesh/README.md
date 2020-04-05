### 2_Check T3S Mesh: Why my mesh gives me bad results?

#### To run:

```
python checkt3smesh.py
```

This code is to visualize the quality of a T3S format finite element mesh. T3S format mesh file is essential for building SELAFIN file in numerical modeling using [TELEMAC](http://www.opentelemac.org/). A CLI format boundary file is optional but recommended if better handling on boundary elements is wanted.

#### Prerequisites:

* Python >= 3.5
* Numpy+Scipy+Matplotlib
* Numba ([nopython=True](https://numba.pydata.org/numba-doc/latest/user/5minguide.html) is on by default)

#### Example:

Enter `example_mesh.t3s` for mesh filename and `example_boundary.cli` for boundary file name. Result would be like this:

![intro](https://github.com/ZhiLiHydro/Self-Use-Handy-Codes/blob/master/2_CheckT3SMesh/example_result.png)

#### To do:

- [X] Add handling on boundary elements
- [ ] Optimize boundary obtuse triangles

