# s3-image-proxy

Tiny [Starlette](https://www.starlette.io/) application for retrieving image files from a private S3 bucket, resizing them based on querystring parameters and serving them with cache headers so the resized images can be cached by a CDN.

See [Using SQL to find my best photo of a pelican according to Apple Photos](https://simonwillison.net/2020/May/21/apple-photos-sqlite/) for background information on this project.

## Demo

You can see a demo of this proxy in action serving images [on this page](https://dogsheep-photos.dogsheep.net/public/photos_with_apple_metadata).

## Configuration

The following environment variables are required:

- `S3_BUCKET`
- `S3_AWS_ACCESS_KEY_ID`
- `S3_AWS_SECRET_ACCESS_KEY`

Here [are some notes](https://github.com/dogsheep/dogsheep-photos/issues/4) on creating an S3 bucket with the right credentials.

If you want to be able to access the original image files, set a `ORIGINAL_TOKEN` with a secret token that you plan to use to access the originals.

## Deployment

You can deploy this tool directly to [Vercel](https://vercel.com/). You'll need to set the necessary environment variables.

Vercel provides a CDN, so resized images should be served very quickly on subsequent requests to the same image.

## Local development

For local development you will need to install an additional dependency: uvicorn.

    pip install -r requirements.txt
    pip install uvicorn

You can then run the server like this:

    S3_AWS_ACCESS_KEY_ID="xxx" \
    S3_AWS_SECRET_ACCESS_KEY="yyy" \
    S3_BUCKET="your-bucket" \
    ORIGINAL_TOKEN="your-secret-token" \
    uvicorn index:app

## Usage

Once up and running, you can access image files stored in the S3 bucket like so:

    http://localhost:8000/i/name-of-file.jpeg

To resize the image, pass ?w= or ?h= arguments:

    http://localhost:8000/i/name-of-file.jpeg?w=400
    http://localhost:8000/i/name-of-file.jpeg?h=400

Use `?bw=1` to convert the image to black and white.

If you are serving JPEGs you can control the quality using `?q=` - e.g. `?q=25` for a lower quality (but faster loading) image.

To access the original image file, use this URL:

    http://localhost:8000/o/name-of-file.jpeg?token=YOUR_SECRET_TOKEN
