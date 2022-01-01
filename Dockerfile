FROM jekyll/jekyll:3.8

WORKDIR /srv/jekyll
COPY Gemfile.lock .
COPY Gemfile .

RUN gem install bundler

RUN bundle install

CMD ["jekyll", "--help"]
ENTRYPOINT ["/usr/jekyll/bin/entrypoint"]
WORKDIR /srv/jekyll
VOLUME  /srv/jekyll
EXPOSE 35729
EXPOSE 4000