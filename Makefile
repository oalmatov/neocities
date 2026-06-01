.PHONY: build serve clean words

words:
	go run ./cmd/generate-words

build: clean
	go run ./cmd/render-poems
	hugo --minify --gc --cleanDestinationDir

serve:
	go run ./cmd/render-poems
	hugo server --disableFastRender

clean:
	rm -rf public resources

new-%:
	hugo new $*/$(slug)/index.md
