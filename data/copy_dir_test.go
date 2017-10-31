package data

import (
	"os"
	"testing"

	"gopkg.in/src-d/go-billy.v3/memfs"
)

func TestCopyDir(t *testing.T) {
	srcFs := memfs.New()
	srcFs.MkdirAll("/src/something/nested", os.ModeDir)
	testFiles := []string{
		"/src/important.txt",
		"/src/doggo.txt",
		"/src/something/else.txt",
		"/src/something/nested/nothingtoseehere.txt",
	}
	for _, f := range testFiles {
		srcFs.Create(f)
	}

	dstFs := memfs.New()

	// sanity check - make sure files don't exist in dstfs before
	for _, f := range testFiles {
		if _, err := dstFs.Stat(f); err == nil {
			t.Fatalf("%s exists in dstFs before copy", f)
		}
	}

	CopyDir(srcFs, dstFs, "/src", "/dst")

	// make sure that all the destination files exist now
	for _, f := range testFiles {
		if _, err := dstFs.Stat(f); os.IsNotExist(err) {
			t.Fatalf("%s does not exist in dstFs after copy", f)
		}
	}
}
