# GitFichas

[![Netlify Status](https://api.netlify.com/api/v1/badges/66b3d264-55b3-4051-a693-49c7107a2b8f/deploy-status)](https://app.netlify.com/sites/gitfichas/deploys)

## Docker stuff

### Building image

```console
docker build -t gitfichas .
```

### Serving

```console
docker run --rm --volume="$PWD:/srv/jekyll"  -p 4001:4000 -it gitfichas jekyll serve --livereload
```

## Credits

### Creator of this template

#### Paul Le

* [www.lenpaul.com](http://lenpaul.com)

* [Twitter](https://twitter.com/paululele)

* [GitHub](https://github.com/LeNPaul)

* [Here's the source repo for the template](https://github.com/lenpaul/portfolio-jekyll-theme/).

## License

Open sourced under the [MIT license](https://github.com/LeNPaul/portfolio-jekyll-theme/blob/gh-pages/LICENSE.md).
