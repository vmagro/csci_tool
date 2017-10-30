package cmd

import (
	"fmt"
)

// Collect subcommand
func Collect(project string) {
	fmt.Printf("Collecting assignments for %s\n", project)
	// shouldComment := viper.Get("CommentOnCollect")
}
