package git

import (
	"github.com/golang/glog"
	"github.com/spf13/viper"
	"github.com/vmagro/csci_tool/data"
	"gopkg.in/src-d/go-billy.v3/memfs"
	git "gopkg.in/src-d/go-git.v4"
	"gopkg.in/src-d/go-git.v4/storage/memory"
)

// Repo represents a local repo on disk (or in memory)
type Repo struct {
	repository *git.Repository
}

// CloneStudentRepo clones a student repo to an in-memory fs
func CloneStudentRepo(s *data.Student) (*Repo, error) {
	repoURL, err := s.RepoURL()
	if err != nil {
		return nil, err
	}
	r, err := git.Clone(memory.NewStorage(), memfs.New(), &git.CloneOptions{
		URL:   repoURL.String(),
		Depth: 1,
	})
	if err != nil {
		return nil, err
	}
	return &Repo{repository: r}, nil
}

// Commit creates a new commit with what is staged in git using the given commit message
func (r *Repo) Commit(message string) {
	author := viper.Get("CommitAuthor")
	glog.Infof("Commiting '%s' as '%s'", message, author)
}

func (r *Repo) Worktree() (*git.Worktree, error) {
	return r.repository.Worktree()
}

// AddDir adds a directory in the working tree to staging
func AddDir(wt *git.Worktree, src string) error {
	srcFs := wt.Filesystem

	files, err := srcFs.ReadDir(src)
	if err != nil {
		return err
	}

	for _, file := range files {
		if file.IsDir() {
			err = AddDir(wt, srcFs.Join(src, file.Name()))
			if err != nil {
				return err
			}
			continue
		}
		wt.Add(srcFs.Join(src, file.Name()))
	}
	return nil
}

// AddAll adds all files in the repo working tree to staging
func AddAll(repo *git.Repository) error {
	wt, err := repo.Worktree()
	if err != nil {
		return err
	}
	return AddDir(wt, "/")
}
