$Word = New-Object -ComObject Word.Application
$Word.Visible = $false

$DocsDir = "d:\Major Project\docs"
$FilesToConvert = @("Project_Report.md", "Comprehensive_Guide.md")

foreach ($File in $FilesToConvert) {
    try {
        $MdPath = Join-Path -Path $DocsDir -ChildPath $File
        $DocxPath = Join-Path -Path $DocsDir -ChildPath ($File.Replace(".md", ".docx"))
        
        Write-Host "Converting $MdPath to $DocxPath"
        
        # Open markdown text as plain text document
        $Doc = $Word.Documents.Open($MdPath)
        
        # SaveAs2 format 16 is wdFormatDocumentDefault (docx)
        $Doc.SaveAs2($DocxPath, 16)
        $Doc.Close()
        
        Write-Host "Success: $DocxPath"
    } catch {
        Write-Host "Failed to convert $File"
        Write-Host $_.Exception.Message
    }
}

$Word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($Word)
Remove-Variable Word
