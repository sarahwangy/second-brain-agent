-- dump_notes.applescript — Apple Notes connector for apple-notes-import skill.
--
-- Walks accounts -> folders (recursively) -> notes, and for each note writes:
--   <outDir>/raw/<index>.html   the note's raw HTML body (verbatim; pandoc normalizes later)
--   <outDir>/meta/<index>.meta  tab-separated metadata (one key<TAB>value per line)
--
-- Robustness choices:
--   * Body HTML is written via AppleScript file I/O (not returned as a string) so arbitrary
--     content — newlines, quotes, emoji, Chinese — can never corrupt a delimiter.
--   * Metadata values are all single-line in Apple Notes (title is the note's first line; folder
--     and account names are single-line), so a key<TAB>value file is safe. Parser must split on the
--     FIRST tab only.
--   * index is a zero-padded sequential counter -> filesystem-safe, collision-free filenames.
--     The real Core Data id is stored inside the .meta file.
--   * Locked (password-protected) notes: body is inaccessible -> body file is empty and meta records
--     locked<TAB>true. The skill reports these as skipped; never silently dropped.
--
-- Usage:  osascript dump_notes.applescript <absolute-output-dir>

on run argv
	if (count of argv) < 1 then error "usage: dump_notes.applescript <absolute-output-dir>"
	set outDir to item 1 of argv
	do shell script "mkdir -p " & quoted form of (outDir & "/raw") & " " & quoted form of (outDir & "/meta")
	set noteIndex to 0
	tell application "Notes"
		repeat with acct in accounts
			set acctName to name of acct
			repeat with f in folders of acct
				set noteIndex to my processFolder(f, acctName, acctName, outDir, noteIndex)
			end repeat
		end repeat
	end tell
	return (noteIndex as string) & " notes dumped to " & outDir
end run

-- Recurse a folder: dump its direct notes, then descend into subfolders.
on processFolder(f, acctName, pathPrefix, outDir, idx)
	tell application "Notes"
		set folderPath to pathPrefix & "/" & (name of f)
		repeat with n in notes of f
			set idx to idx + 1
			my dumpNote(n, acctName, folderPath, outDir, idx)
		end repeat
		repeat with sub in folders of f
			set idx to my processFolder(sub, acctName, folderPath, outDir, idx)
		end repeat
	end tell
	return idx
end processFolder

on dumpNote(n, acctName, folderPath, outDir, idx)
	tell application "Notes"
		set isLocked to false
		try
			set isLocked to password protected of n
		end try
		set noteTitle to ""
		try
			set noteTitle to name of n
		end try
		set noteId to ""
		try
			set noteId to id of n as string
		end try
		set createdDate to ""
		try
			set createdDate to (creation date of n) as string
		end try
		set modDate to ""
		try
			set modDate to (modification date of n) as string
		end try
		set attCount to 0
		try
			set attCount to count of attachments of n
		end try
		set bodyHtml to ""
		if not isLocked then
			try
				set bodyHtml to body of n
			end try
		end if
	end tell

	set pad to my pad4(idx)
	my writeFile(outDir & "/raw/" & pad & ".html", bodyHtml)

	set metaText to "index" & tab & pad & linefeed
	set metaText to metaText & "id" & tab & noteId & linefeed
	set metaText to metaText & "account" & tab & acctName & linefeed
	set metaText to metaText & "folder" & tab & folderPath & linefeed
	set metaText to metaText & "title" & tab & noteTitle & linefeed
	set metaText to metaText & "created" & tab & createdDate & linefeed
	set metaText to metaText & "modified" & tab & modDate & linefeed
	set metaText to metaText & "attachments" & tab & (attCount as string) & linefeed
	set metaText to metaText & "locked" & tab & (isLocked as string) & linefeed
	my writeFile(outDir & "/meta/" & pad & ".meta", metaText)
end dumpNote

on pad4(i)
	set s to i as string
	repeat while (length of s) < 4
		set s to "0" & s
	end repeat
	return s
end pad4

on writeFile(thePath, theText)
	set f to open for access (POSIX file thePath) with write permission
	try
		set eof of f to 0
		write theText to f as «class utf8»
	end try
	close access f
end writeFile
