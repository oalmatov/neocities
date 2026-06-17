.PHONY: build serve clean words

words:
	go run ./cmd/generate-words

build: clean
	go run ./cmd/render-poems
	go run ./cmd/feed-sentiment
	hugo --minify --gc --cleanDestinationDir

serve:
	go run ./cmd/render-poems
	go run ./cmd/feed-sentiment
	hugo server --disableFastRender

clean:
	rm -rf public resources

new-%:
	hugo new $*/$(slug)/index.md
