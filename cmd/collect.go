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
	"github.com/spf13/viper"
	"github.com/vmagro/csci_tool/data"
	billy "gopkg.in/src-d/go-billy.v3"
	"gopkg.in/src-d/go-billy.v3/memfs"
	git "gopkg.in/src-d/go-git.v4"
	"gopkg.in/src-d/go-git.v4/plumbing"
	"gopkg.in/src-d/go-git.v4/plumbing/object"
	"gopkg.in/src-d/go-git.v4/storage/memory"
)

func ListDir(srcFs billy.Filesystem, src string) {
	files, _ := srcFs.ReadDir(src)

	for _, file := range files {
		if file.IsDir() {
			ListDir(srcFs, srcFs.Join(src, file.Name()))
			continue
		}
		fmt.Println(srcFs.Join(src, file.Name()))
	}
}

// CollectStudent clones the proper commit from a student repo and copies it's project files to the
// submissions repo.
func CollectStudent(student *data.Student, deadline time.Time, project string, github *data.Github, submissions *git.Worktree) error {
	commit, err := github.LatestCommitBefore(student, deadline)
	if err != nil {
		return err
	}
	fmt.Printf("Collecting from %s using commit %s\n", student, *commit.SHA)

	// clone the repo into memory, then copy it's files into the other in-memory FS
	repo, err := data.CloneStudentRepo(student)
	if err != nil {
		return err
	}
	wt, err := repo.Worktree()
	wt.Checkout(&git.CheckoutOptions{
		Hash: plumbing.NewHash(*commit.SHA),
	})
	if err != nil {
		return err
	}

	err = data.CopyDir(wt.Filesystem, submissions.Filesystem, project, student.UnixName)
	if err != nil {
		return err
	}
	ListDir(wt.Filesystem, project)
	ListDir(submissions.Filesystem, "/")
	_, err = submissions.Add("smagro/rtarget")
	if err != nil {
		return fmt.Errorf("Couldn't add %s to git: %s", student.UnixName, err)
	}
	return nil
}

// collectCmd represents the collect command
var collectCmd = &cobra.Command{
	Use:   "collect project [deadline]",
	Short: "Collect commits from all students",
	Long: `Collect latest commits from all students with an optional deadline (in RFC3339 format).

The given project/directory name will be used in a comment on the student's repos and will be the
only files retained.

csci will clone each student's repo at the latest commit before the deadline and copy the files
under <repo>/<project-name> to a separate directory for later grading.

Examples:

Collect project-1 using the latest commit before the current time
  csci collect project-1

Collect project-2 using the latest commit before Sunday October 29th at 23:59:59PM PDT
  csci collect project-2 "2017-10-29T23:59:59-07:00"
`,
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

		// Try to create a repo to hold the submissions for this assignment if it doesn't exist already
		glog.Infof("Connecting to the GitHub API")
		github := data.NewGithub()
		submissionsRepo, err := github.CreateRepoIfNotExists(fmt.Sprintf("submissions_%s", project))
		if err != nil {
			glog.Fatalf("Failed to get/create submissions repo on Github: %s", err)
		}
		fmt.Printf("Storing submissions in Github repo '%s'\n", *submissionsRepo.FullName)
		// clone the submissions repo into an in-memory fs
		submissionsClone, err := git.Clone(memory.NewStorage(), memfs.New(), &git.CloneOptions{
			URL:   data.CloneableURL(submissionsRepo),
			Depth: 1,
		})
		if err != nil {
			glog.Fatalf("Failed to clone submissions repo: %s", err)
		}
		submissionsWorktree, err := submissionsClone.Worktree()
		if err != nil {
			glog.Fatalf("Failed to open submissions repo working tree: %s", err)
		}

		students, err := data.LoadStudents()
		if err != nil {
			glog.Fatalf("Failed to load students: %s", err)
		}
		fmt.Printf("Collecting from %d students\n", len(students))
		for _, student := range students {
			err = CollectStudent(student, deadline, project, github, submissionsWorktree)
			if err != nil {
				fmt.Printf("Failed to collect from %s (%s)\n", student, err)
			}
		}

		fmt.Println("Pushing submissions to GitHub")
		_, err = submissionsWorktree.Commit(fmt.Sprintf("Submissions with deadline %s", deadline), &git.CommitOptions{
			Author: &object.Signature{
				Name:  viper.GetString("BotUsername"),
				Email: viper.GetString("BotEmail"),
				When:  time.Now(),
			},
		})
		if err != nil {
			glog.Fatalf("Failed to commit changes to submissions repo: %s", err)
		}
		// err = submissionsClone.Push(&git.PushOptions{})
		// if err != nil {
		// 	glog.Fatalf("Failed to push changes to submissions repo: %s", err)
		// }
	},
	Args: cobra.RangeArgs(1, 2),
}

func init() {
	RootCmd.AddCommand(collectCmd)
}
