# cougar-or-not

My first attempt at a machine learning API, using a pre-calculated model trained using [iNaturalist](https://www.inaturalist.org/) data.

The resulting API is used by the [@critter_vision](https://twitter.com/critter_vision) Twitter bot, the source code for which can be found at https://github.com/natbat/CritterVision

The model is `usa-inaturalist-cats.pth` - an 83MB file.

The notebook `inaturalist-cats.ipynb` shows how I trained the model, using [fastai](https://github.com/fastai/fastai).

`cougar.py` is a very tiny [Starlette](https://www.starlette.io/) API server which simply accepts file image uploads and runs them against the pre-calculated model.

It also accepts a URL to an image, e.g. https://cougar-or-not.now.sh/classify-url?url=https://upload.wikimedia.org/wikipedia/commons/9/9a/Oregon_Cougar_ODFW.JPG

The `Dockerfile` means the entire thing can be deployed to [Zeit Now](https://zeit.co/now) or any other container hosting service.

## Examples

Cougar: https://cougar-or-not.now.sh/classify-url?url=https://upload.wikimedia.org/wikipedia/commons/9/9a/Oregon_Cougar_ODFW.JPG

<img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Oregon_Cougar_ODFW.JPG">

Bobcat: https://cougar-or-not.now.sh/classify-url?url=https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Bobcat2.jpg/1200px-Bobcat2.jpg

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Bobcat2.jpg/1200px-Bobcat2.jpg">
