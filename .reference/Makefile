.PHONY: all

clear_translated:
	@find . -name '*_translated.md' -delete

clear_temp:
	@find . -name '*.md.tmp' -delete

clear: clear_translated clear_temp

format:
	@mdformat . --wrap=no
