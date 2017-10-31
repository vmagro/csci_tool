package data

import (
	"io"

	billy "gopkg.in/src-d/go-billy.v3"
)

// CopyDir recursively copies directories between billy filesystems srcFs -> dstFs
// src, dst are strings representing the paths within their respective filesystems
func CopyDir(srcFs, dstFs billy.Filesystem, src, dst string) error {
	files, err := srcFs.ReadDir(src)
	if err != nil {
		return err
	}

	for _, file := range files {
		if file.IsDir() {
			// recurse!
			dstFs.MkdirAll(dstFs.Join(dst, file.Name()), file.Mode())
			err = CopyDir(srcFs, dstFs, srcFs.Join(src, file.Name()), dstFs.Join(dst, file.Name()))
			if err != nil {
				return err
			}
			continue
		}

		// it's a file - make a new one then copy it
		dstFile, err := dstFs.Create(dstFs.Join(dst, file.Name()))
		if err != nil {
			return err
		}
		srcFile, err := srcFs.Open(srcFs.Join(src, file.Name()))
		if err != nil {
			return err
		}
		io.Copy(dstFile, srcFile)
	}
	return nil
}
