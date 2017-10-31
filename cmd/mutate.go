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

	"github.com/spf13/cobra"
)

// mutateCmd represents the mutate command
var mutateCmd = &cobra.Command{
	Use:   "mutate",
	Short: "Mutate student repos by running 'plugin' code",
	Long: `Mutate makes changes to student repos by running an external program/executable named
'mutate' in the project directory of the assignments repo. 'mutate' must be executable but can be
implemented in any programming language.
'mutate' will be run as follows:
	./mutate student_unix_name student_id student_repo_dir
		student_unix_name is the first portion of an @usc.edu email
		student_id is the USC ID
		student_repo_dir is the path to the project directory in a temporary clone

	It is up to the 'mutate' program to make any necessary modifications to the repo, 'git commit' and
		'git push'
	A non-zero exit code will be recorded as a failure and the student will be logged to csci logs.
`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("mutate called")
	},
}

func init() {
	RootCmd.AddCommand(mutateCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// mutateCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// mutateCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
