.PHONY: build serve clean

build: clean
	go run ./cmd/render-poems
	hugo --minify --gc --cleanDestinationDir

serve:
	go run ./cmd/render-poems
	hugo server

clean:
	rm -rf public resources

new-%:
	hugo new $*/$(slug)/index.md
