require 'pathname'

module Jekyll
  module UrlRelativizer
    def relative_url(url)
      pageUrl = @context.registers[:page]["url"]
      if url.end_with?("/")
        url += "index.html"
      end
      if not pageUrl.end_with?("/")
      	pageUrl = Pathname(pageUrl).parent
      end
      if url.start_with?("/")
        Pathname(url).relative_path_from(Pathname(pageUrl)).to_s
      else
        url
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::UrlRelativizer)
