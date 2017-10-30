package data

import (
	"github.com/golang/glog"
	"github.com/spf13/viper"
	git "gopkg.in/src-d/go-git.v4"
	"gopkg.in/src-d/go-git.v4/storage/memory"
)

// Repo represents a local repo on disk (or in memory)
type Repo struct {
	repository *git.Repository
}

// CloneRepo clones a student repo to an in-memory fs
func CloneRepo(s *Student) (*Repo, error) {
	repoURL, err := s.RepoURL()
	if err != nil {
		return nil, err
	}
	r, err := git.Clone(memory.NewStorage(), nil, &git.CloneOptions{
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
