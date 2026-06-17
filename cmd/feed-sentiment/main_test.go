package main

import (
	"testing"
	"time"
)

func TestStripRemovesFrontMatterImagesShortcodesAndUnwrapsLinks(t *testing.T) {
	raw := "---\ndate: 2026-06-04T10:16:20-07:00\n---\n\n" +
		"![a photo](cappuccino.jpeg)\n\n" +
		"a cappuccino because oh how i long for [innocence](https://example.com)\n\n" +
		"{{< carousel >}}\n![x](a.jpeg)\n{{< /carousel >}}\n" +
		"a few days ago my money tree was shedding leaves"

	got := strip(raw)

	for _, banned := range []string{"---", "date:", "![", "{{<", "https://example.com", ".jpeg"} {
		if contains(got, banned) {
			t.Fatalf("strip output still contains %q:\n%s", banned, got)
		}
	}
	if !contains(got, "a cappuccino because oh how i long for innocence") {
		t.Fatalf("strip dropped prose / link text:\n%s", got)
	}
	if !contains(got, "money tree was shedding leaves") {
		t.Fatalf("strip dropped post-shortcode prose:\n%s", got)
	}
}

func TestStripReturnsEmptyForImageOnlyBody(t *testing.T) {
	raw := "---\ndate: 2026-01-01\n---\n\n![only an image](pic.jpeg)\n"
	if got := strip(raw); got != "" {
		t.Fatalf("expected empty prose, got %q", got)
	}
}

func TestParseDate(t *testing.T) {
	raw := "---\ndate: 2026-04-23T09:25:06-07:00\n---\nbody"
	got := parseDate(raw)
	want := time.Date(2026, 4, 23, 9, 25, 6, 0, time.FixedZone("", -7*3600))
	if !got.Equal(want) {
		t.Fatalf("parseDate = %v, want %v", got, want)
	}
	if !parseDate("no front matter").IsZero() {
		t.Fatalf("expected zero time for missing date")
	}
}

func TestParseDateSpaceSeparatedNoTimezone(t *testing.T) {
	got := parseDate("---\ndate: 2026-04-20 22:48:00\n---\nbody")
	if got.IsZero() {
		t.Fatal("expected space-separated date to parse, got zero time")
	}
	if got.Year() != 2026 || got.Month() != time.April || got.Day() != 20 {
		t.Fatalf("parseDate = %v, want 2026-04-20", got)
	}
}

func TestHappinessMapping(t *testing.T) {
	cases := map[float64]int{-1.0: 0, 0.0: 50, 1.0: 100}
	for compound, want := range cases {
		if got := happiness(compound); got != want {
			t.Fatalf("happiness(%v) = %d, want %d", compound, got, want)
		}
	}
}

func contains(haystack, needle string) bool {
	return len(needle) == 0 || (len(haystack) >= len(needle) && indexOf(haystack, needle) >= 0)
}

func indexOf(haystack, needle string) int {
	for i := 0; i+len(needle) <= len(haystack); i++ {
		if haystack[i:i+len(needle)] == needle {
			return i
		}
	}
	return -1
}
