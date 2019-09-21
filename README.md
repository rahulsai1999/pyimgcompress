## To build and deploy

``` docker build -t pyimgcompress . ```

``` heroku container:login ```

``` heroku container:push web --app pyimgcompress ```

``` heroku container:release web --app pyimgcompress ```

