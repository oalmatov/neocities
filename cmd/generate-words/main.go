// Picks random words from the magnet-poetry pools and rewrites the
// INITIAL_WORDS block in layouts/fridge-poems/list.html, scattering each
// word across the fridge canvas with a random position and rotation.
//
// Word pools sourced from https://github.com/sadgrlonline/magnetic-poetry
package main

import (
	"flag"
	"fmt"
	"log"
	"math/rand/v2"
	"os"
	"regexp"
	"sort"
	"strings"
)

const (
	canvasWidth  = 1136
	canvasHeight = 900
)

var common = []string{
	"a", "an", "the", "there", "is", "these", "those", "are", "they", "their",
	"she", "her", "he", "his", "me", "let", "I", "for", "am", "you", "because",
	"if", "be", "to", "too", "of", "in", "have", "first", "not", "on", "as",
	"at", "but", "by", "do", "from", "or", "will", "so", "get", "give", "would",
	"could", "should", "was", "go", "might", "were", "your", "us", "we", "them",
	"like", "let's", "and", "oh", "myself", "yourself", "anything", "nothing",
	"everything", "who", "what", "when", "come", "came", "where", "why", "won't",
	"see", "my", "more", "no", "want",
}

var nouns = []string{
	"tree", "leaf", "star", "rose", "thing", "mushroom", "toadstool", "willow",
	"canopy", "witch", "goddess", "mother", "stillness", "mistress", "stream",
	"meadow", "deer", "pond", "gate", "crystal", "river", "cave", "mystery",
	"cliff", "forest", "woods", "chains", "bat", "owl", "butterfly", "moth",
	"serpent", "mermaid", "frog", "toad", "creature", "wolf", "cat", "bird",
	"fog", "wing", "insect", "critter", "poison", "rainwater", "storm", "weapon",
	"hunger", "acid", "wood", "passion", "moon", "garden", "vine", "iris",
	"azalea", "pine", "petal", "dawn", "vision", "sky", "throat", "cloud",
	"bough", "lilac", "silver", "cream", "strength", "desert", "light", "shadow",
	"dew", "myth", "sea-foam", "honey", "nectar", "face", "gloam", "body",
	"weakness", "pollen", "snow", "savage", "sand", "mist", "tea", "bark",
	"rebirth", "death", "eternity", "mercy", "mouth", "blood", "sword", "spirit",
	"burial", "destruction", "elixir", "teeth", "scent", "morning", "evening",
	"night", "tide", "seawater", "coffee", "neck", "glass", "pearl", "monster",
	"flower", "earth", "woman", "shield", "pattern", "hole", "dessert", "salt",
	"hope", "temple", "space", "serendipity", "bubble", "twilight", "growth",
	"hand", "war", "limit", "outside", "violence", "sorrow", "stem", "cowardice",
	"sandbar", "dusk", "eyes", "life", "mind", "blossom", "labor", "voice",
	"honeydew", "unknown", "sunbeam", "home", "moment", "warrior", "day", "gum",
	"midday", "catharsis", "tongue", "haze", "birth", "afternoon", "pain",
	"wilderness", "lagoon", "planet", "arch",
}

var verbs = []string{
	"hang", "say", "tell", "ask", "caught", "find", "shine", "listen", "glitter",
	"nestle", "flicker", "glow", "form", "cloak", "walk", "fade", "sparkle",
	"cling", "shape", "dig", "hover", "remind", "pulse", "break", "crawl",
	"smile", "hold", "create", "drift", "crack", "stay", "drip", "flash",
	"sweep", "know", "writhe", "bloom", "brim", "awake", "asleep", "grow",
	"bask", "fold", "split", "splinter", "ignite", "illuminate", "intensify",
	"gravitate", "clutch", "cower", "lie", "swallow", "soar", "shrivel",
	"shimmer", "crunch", "float", "breathe", "weave", "make", "crush", "bounce",
	"veil", "soak", "shrink", "warp", "reflect", "reach", "tremble", "whisper",
	"haunt", "bend", "pulsate", "push", "obliterate", "smooth", "roam", "love",
	"dive", "crash", "settle", "stretch", "blink", "awaken", "rush", "curl",
	"pull", "glide", "embrace", "lurch", "electrify", "roar", "squeeze", "grasp",
	"fragment", "catapult", "surrender", "march", "howl", "decay", "growl",
	"groan", "smell", "look", "forgive", "scream", "weep", "devastate",
	"shatter", "watch", "dance", "touch", "show", "believe",
}

var adjectives = []string{
	"cool", "pale", "sharp", "sacred", "beautiful", "dark", "infinite",
	"unhurried", "flat", "strange", "outer", "fair", "fresh", "quiet", "dear",
	"empty", "magical", "pretty", "deep", "dying", "uninterrupted", "round",
	"crimson", "young", "other", "alive", "patient", "starless", "cheap",
	"feral", "brittle", "tight", "half-lit", "cascading", "full", "bright",
	"fringed", "forbidden", "tangled", "sunless", "twisted", "unsteady",
	"mystical", "silken", "soft", "still", "sweet", "warm", "short", "open",
	"unsettled", "sleepy", "powerful", "perfumed", "wet", "burnt", "long",
	"snowy", "thick", "stagnant", "purple", "black", "green", "pink", "yellow",
	"blue", "red", "orange", "violet", "loose", "broken", "milky", "unyielding",
	"bleak", "bewitched", "bruised", "cloudy", "cruel", "deadly", "dry",
	"electric", "fearless", "frozen", "funny", "glistening", "glossy", "growing",
	"hasty", "hollow", "hoarse", "hot", "hungry", "idle", "knowing", "leafy",
	"lost", "low", "melodic", "mild", "misty", "modest", "muddy", "mysterious",
	"necessary", "new", "normal", "obvious", "old", "plump", "proud", "pure",
	"raw", "rich", "ripe", "sandy", "scarce", "shimmering", "slight", "small",
	"steel", "tender", "thorny", "tired", "twin", "useful", "vacant", "vivid",
	"warlike", "weak", "weird", "wild", "wooden",
}

var adverbs = []string{
	"warmly", "barely", "sleepily", "sadly", "slowly", "here", "clumsily",
	"curiously", "wistfully", "farthest", "endlessly", "darkest", "boldly",
	"brightly", "terribly", "always", "sickly", "often", "tomorrow", "quickly",
	"safely", "quietly", "wildly", "hard", "fast", "bravely", "however",
	"nonetheless", "clearly", "easily", "fiercely", "foolishly", "heavily",
	"wisely", "wearily", "unwillingly", "ultimately", "suddenly", "shakily",
	"seemingly", "rarely", "obediently", "naturally", "increasingly",
	"noiselessly", "deafeningly", "weakly", "cruelly",
}

var prepositions = []string{
	"above", "about", "around", "between", "despite", "except", "without",
	"beside", "among", "beneath", "across", "before", "behind", "below", "onto",
	"inside", "under", "up", "with", "over", "away", "along", "next",
	"underneath", "until", "within", "toward",
}

// bound is a word pool with a min/max count of words drawn from it.
type bound struct {
	name string
	pool []string
	min  int
	max  int
}

// bounds is ordered so the total of mins <= numWords <= total of maxes.
var bounds = []bound{
	{"common", common, 4, 8},
	{"nouns", nouns, 6, 11},
	{"verbs", verbs, 4, 8},
	{"adjectives", adjectives, 3, 7},
	{"adverbs", adverbs, 1, 4},
	{"prepositions", prepositions, 1, 4},
}

type word struct {
	text     string
	x        int
	y        int
	rotation float64
}

// pickCounts assigns a per-pool count within each pool's bounds, totalling n.
func pickCounts(n int) map[string]int {
	counts := map[string]int{}
	total := 0
	for _, b := range bounds {
		counts[b.name] = b.min
		total += b.min
	}

	remaining := n - total
	for remaining > 0 {
		candidates := []bound{}
		for _, b := range bounds {
			if counts[b.name] < b.max {
				candidates = append(candidates, b)
			}
		}
		if len(candidates) == 0 {
			break
		}

		choice := candidates[rand.IntN(len(candidates))]
		counts[choice.name]++
		remaining--
	}

	return counts
}

// pickWords draws n words across the pools and scatters them on the canvas.
func pickWords(n int) []word {
	counts := pickCounts(n)

	chosen := []string{}
	for _, b := range bounds {
		picks := rand.Perm(len(b.pool))[:counts[b.name]]
		for _, i := range picks {
			chosen = append(chosen, b.pool[i])
		}
	}
	rand.Shuffle(len(chosen), func(i, j int) { chosen[i], chosen[j] = chosen[j], chosen[i] })

	words := make([]word, len(chosen))
	for i, text := range chosen {
		words[i] = word{
			text:     text,
			x:        rand.IntN(canvasWidth-80-20+1) + 20,
			y:        rand.IntN(canvasHeight-30-20+1) + 20,
			rotation: float64(rand.IntN(61))/10 - 3, // [-3.0, 3.0] in 0.1 steps
		}
	}

	return words
}

// formatBlock renders the words as the JS INITIAL_WORDS literal, matching the
// surrounding template's indentation (4 spaces for the statement, 6 for items).
func formatBlock(words []word) string {
	var b strings.Builder
	b.WriteString("const INITIAL_WORDS = [\n")
	for _, w := range words {
		fmt.Fprintf(&b, "      {text: %q, x: %d, y: %d, rotation: %.1f},\n",
			w.text, w.x, w.y, w.rotation)
	}
	b.WriteString("    ];")

	return b.String()
}

func main() {
	numWords := flag.Int("n", 35, "number of magnet words to scatter")
	path := flag.String("path", "layouts/fridge-poems/list.html", "template file to rewrite")
	flag.Parse()

	html, err := os.ReadFile(*path)
	if err != nil {
		log.Fatal(err)
	}

	words := pickWords(*numWords)
	block := formatBlock(words)

	re := regexp.MustCompile(`(?s)const INITIAL_WORDS = \[.*?\];`)
	if !re.Match(html) {
		log.Fatalf("%s: no INITIAL_WORDS block found", *path)
	}

	updated := re.ReplaceAllLiteralString(string(html), block)
	if err := os.WriteFile(*path, []byte(updated), 0644); err != nil {
		log.Fatal(err)
	}

	texts := make([]string, len(words))
	for i, w := range words {
		texts[i] = w.text
	}
	sort.Strings(texts)
	fmt.Printf("scattered %d words: %s\n", len(words), strings.Join(texts, ", "))
}
