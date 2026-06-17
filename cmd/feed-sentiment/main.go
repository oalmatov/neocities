// Reads content/feed/*/index.md, scores each post's "happiness" (0-100) via
// VADER, and writes data/feed_sentiment.json (sorted ascending by date) for the
// homepage chart. Mirrors cmd/render-poems conventions.
package main

import (
	"encoding/json"
	"log"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"

	"github.com/jonreiter/govader"
)

type Entry struct {
	Slug      string `json:"slug"`
	Date      string `json:"date"`
	Happiness int    `json:"happiness"`
}

type scored struct {
	entry Entry
	date  time.Time
}

var (
	frontMatter = regexp.MustCompile(`(?s)^---.*?---`)
	shortcode   = regexp.MustCompile(`{{<.*?>}}`)
	image       = regexp.MustCompile(`!\[[^\]]*\]\([^)]*\)`)
	link        = regexp.MustCompile(`\[([^\]]*)\]\([^)]*\)`)
	dateLine    = regexp.MustCompile(`(?m)^date:\s*(.+)$`)
)

// strip turns a post body into bare prose for the analyzer.
func strip(raw string) string {
	text := frontMatter.ReplaceAllString(raw, "")
	text = image.ReplaceAllString(text, "")
	text = shortcode.ReplaceAllString(text, "")
	text = link.ReplaceAllString(text, "$1")

	return strings.TrimSpace(text)
}

func parseDate(raw string) time.Time {
	match := dateLine.FindStringSubmatch(raw)
	if match == nil {
		return time.Time{}
	}

	value := strings.TrimSpace(match[1])
	for _, layout := range []string{time.RFC3339, "2006-01-02T15:04:05-07:00", "2006-01-02 15:04:05", "2006-01-02"} {
		if parsed, err := time.Parse(layout, value); err == nil {
			return parsed
		}
	}

	return time.Time{}
}

func happiness(compound float64) int {
	value := int(math.Round((compound + 1) / 2 * 100))
	if value < 0 {
		return 0
	}
	if value > 100 {
		return 100
	}

	return value
}

func main() {
	analyzer := govader.NewSentimentIntensityAnalyzer()

	entries, err := os.ReadDir("content/feed")
	if err != nil {
		log.Fatal(err)
	}

	var posts []scored
	for _, dirEntry := range entries {
		if !dirEntry.IsDir() {
			continue
		}

		path := filepath.Join("content/feed", dirEntry.Name(), "index.md")
		raw, err := os.ReadFile(path)
		if err != nil {
			continue
		}

		text := strip(string(raw))
		date := parseDate(string(raw))
		if text == "" || date.IsZero() {
			continue
		}

		score := analyzer.PolarityScores(text)
		posts = append(posts, scored{
			entry: Entry{
				Slug:      dirEntry.Name(),
				Date:      date.Format(time.RFC3339),
				Happiness: happiness(score.Compound),
			},
			date: date,
		})
	}

	sort.Slice(posts, func(i, j int) bool { return posts[i].date.Before(posts[j].date) })

	result := make([]Entry, 0, len(posts))
	for _, post := range posts {
		result = append(result, post.entry)
	}

	output, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	if err := os.WriteFile("data/feed_sentiment.json", append(output, '\n'), 0644); err != nil {
		log.Fatal(err)
	}

	log.Printf("wrote data/feed_sentiment.json (%d posts)", len(result))
}
