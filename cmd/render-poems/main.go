// Reads data/poems/*.json and writes:
//
//	static/poems/<slug>.svg          (rendered tile)
//	data/poems_manifest.yaml         (ordered list of months for the home template)
package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"html"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

const (
	canvasWidth  = 1136
	canvasHeight = 900
)

type Word struct {
	Text     string  `json:"text"`
	X        float64 `json:"x"`
	Y        float64 `json:"y"`
	Rotation float64 `json:"rotation"`
}

type Poem struct {
	Name    string `json:"name"`
	Website string `json:"website"`
	Date    string `json:"date"`
	Words   []Word `json:"words"`
}

type Entry struct {
	Slug    string `yaml:"slug"`
	Date    string `yaml:"date"`
	Name    string `yaml:"name,omitempty"`
	Website string `yaml:"website,omitempty"`
}

type Month struct {
	Label string  `yaml:"label"`
	Poems []Entry `yaml:"poems"`
}

type Manifest struct {
	Months []Month `yaml:"months"`
}

func renderSVG(p Poem, textureURI string) string {
	var b strings.Builder
	fmt.Fprintf(&b,
		`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet">`+
			`<image href="%s" width="%d" height="%d" preserveAspectRatio="xMidYMid slice"/>`,
		canvasWidth, canvasHeight, textureURI, canvasWidth, canvasHeight)
	for _, w := range p.Words {
		width := float64(len(w.Text))*9 + 20
		fmt.Fprintf(&b,
			`<g transform="translate(%g,%g) rotate(%g)">`+
				`<rect width="%g" height="24" fill="#faf7ef" stroke="black" stroke-width="1.5"/>`+
				`<text x="%g" y="16" text-anchor="middle" font-family="serif" font-size="14" fill="black">%s</text>`+
				`</g>`,
			w.X, w.Y, w.Rotation, width, width/2, html.EscapeString(w.Text))
	}
	b.WriteString("</svg>")
	return b.String()
}

func main() {
	texture, err := os.ReadFile("static/assets/refrigerator-texture.jpg")
	if err != nil {
		log.Fatal(err)
	}
	textureURI := "data:image/jpeg;base64," + base64.StdEncoding.EncodeToString(texture)

	files, err := filepath.Glob("data/poems/*.json")
	if err != nil {
		log.Fatal(err)
	}
	if err := os.MkdirAll("static/poems", 0755); err != nil {
		log.Fatal(err)
	}

	type rendered struct {
		Entry
		monthLabel string
	}
	var all []rendered

	for _, f := range files {
		data, err := os.ReadFile(f)
		if err != nil {
			log.Fatal(err)
		}
		var p Poem
		if err := json.Unmarshal(data, &p); err != nil {
			log.Fatalf("%s: %v", f, err)
		}

		slug := strings.TrimSuffix(filepath.Base(f), ".json")
		if err := os.WriteFile("static/poems/"+slug+".svg", []byte(renderSVG(p, textureURI)), 0644); err != nil {
			log.Fatal(err)
		}

		t, err := time.Parse(time.RFC3339, p.Date)
		if err != nil {
			log.Fatalf("%s: bad date %q", f, p.Date)
		}
		all = append(all, rendered{
			Entry:      Entry{Slug: slug, Date: p.Date, Name: p.Name, Website: p.Website},
			monthLabel: t.Format("January 2006"),
		})
	}

	// Most-recent-first, then group by month preserving that order.
	sort.Slice(all, func(i, j int) bool { return all[i].Date > all[j].Date })

	var manifest Manifest
	monthIdx := map[string]int{}
	for _, r := range all {
		i, seen := monthIdx[r.monthLabel]
		if !seen {
			i = len(manifest.Months)
			monthIdx[r.monthLabel] = i
			manifest.Months = append(manifest.Months, Month{Label: r.monthLabel})
		}
		manifest.Months[i].Poems = append(manifest.Months[i].Poems, r.Entry)
	}

	out, err := yaml.Marshal(manifest)
	if err != nil {
		log.Fatal(err)
	}
	if err := os.WriteFile("data/poems_manifest.yaml", out, 0644); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("rendered %d poems\n", len(all))
}
