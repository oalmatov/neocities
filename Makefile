.PHONY: build serve clean

build:
	go run ./cmd/render-poems
	hugo --minify

serve:
	go run ./cmd/render-poems
	hugo server

clean:
	rm -rf public resources

new-%:
	hugo new $*/$(slug)/index.md
