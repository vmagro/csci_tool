// Copyright © 2017 Vinnie Magro <v@vinnie.io>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"
	"time"

	"github.com/golang/glog"
	"github.com/spf13/cobra"
)

// collectCmd represents the collect command
var collectCmd = &cobra.Command{
	Use:   "collect project [deadline]",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		project := args[0]
		deadline := time.Now()
		if len(args) > 1 {
			var err error
			deadline, err = time.Parse(time.RFC3339, args[1])
			if err != nil {
				glog.Fatalf("Failed to parse deadline timestamp: %s", err)
			}
		}
		fmt.Printf("Collecting latest commits before \"%s\" for \"%s\"\n", deadline.Format("Mon Jan _2 15:04:05 MST"), project)
	},
	Args: cobra.RangeArgs(1, 2),
}

func init() {
	RootCmd.AddCommand(collectCmd)
}
