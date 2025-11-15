# Citation and Reference Guide

This document explains how to use the reference files provided for your phishing risk detection thesis.

## Available Reference Files

### 1. `REFERENCES.md`
- **Format**: APA 7th Edition (Markdown)
- **Best for**: 
  - Word processors (Microsoft Word, Google Docs)
  - General thesis writing
  - Quick reference and manual citation
  - Most business and social science programs

### 2. `references.bib`
- **Format**: BibTeX
- **Best for**: 
  - LaTeX/Overleaf documents
  - Reference managers (Zotero, Mendeley, EndNote)
  - Computer science and engineering theses
  - Automated citation management

---

## How to Use

### Using REFERENCES.md (APA Format)

**For Microsoft Word:**
1. Open `REFERENCES.md` in any text editor
2. Copy the references you need
3. Paste into your Word document
4. Format as needed (the references are already in APA 7th edition format)

**For Google Docs:**
1. Same process as Word
2. Consider using Google Docs add-ons like "Paperpile" for citation management

**Manual Citation:**
- Each reference is properly formatted in APA style
- Simply copy-paste the entire reference into your bibliography section
- Maintain alphabetical order by author surname

---

### Using references.bib (BibTeX Format)

**For LaTeX/Overleaf:**

1. **Add to your LaTeX project:**
   ```latex
   \documentclass{article}
   \usepackage[style=apa,backend=biber]{biblatex}
   \addbibresource{references.bib}
   
   \begin{document}
   % Your content here
   
   According to \textcite{khonji2013}, phishing detection...
   
   \printbibliography
   \end{document}
   ```

2. **Compile your document:**
   - Run LaTeX
   - Run Biber (or BibTeX)
   - Run LaTeX twice more

**For Zotero:**
1. File → Import → Select `references.bib`
2. All references will be imported automatically
3. Use Zotero plugin in Word/Google Docs for citations

**For Mendeley:**
1. File → Import → BibTeX (*.bib)
2. Select `references.bib`
3. Use Mendeley Citation Plugin for inserting citations

**For EndNote:**
1. File → Import → File
2. Import Option: BibTeX
3. Select `references.bib`

---

## Citation Examples

### APA In-text Citations

**Single author:**
- Narrative: Hong (2012) argues that...
- Parenthetical: ...phishing attacks are increasing (Hong, 2012).

**Two authors:**
- Narrative: Khonji and Iraqi (2013) found that...
- Parenthetical: ...detection methods vary (Khonji & Iraqi, 2013).

**Three or more authors:**
- First citation: Gupta, Tewari, Jain, and Agrawal (2017)...
- Subsequent: Gupta et al. (2017)...

### BibTeX Citations in LaTeX

```latex
% Narrative citation
\textcite{khonji2013} showed that...

% Parenthetical citation
...is well documented \parencite{hong2012}.

% Multiple citations
...as shown in several studies \parencite{khonji2013,hong2012,gupta2017}.

% Citation with page number
...according to \textcite[p. 75]{hong2012}...
```

---

## Reference Categories

Our bibliography includes:

### 1. **Journal Articles** (40+ sources)
- Peer-reviewed research on phishing detection
- Machine learning and cybersecurity journals
- Deep learning and neural network papers

### 2. **Conference Proceedings** (30+ sources)
- ACM SIGKDD, CHI, WWW conferences
- IEEE security conferences
- NIPS/NeurIPS proceedings

### 3. **Books and Book Chapters**
- Deep learning textbooks (Goodfellow et al., 2016)
- Cybersecurity handbooks
- Machine learning references

### 4. **Datasets**
- Enron Email Dataset
- PhishTank
- PhishStorm
- UCI Machine Learning Repository

### 5. **Software Libraries**
- Python: pandas, scikit-learn, NumPy
- Deep Learning: TensorFlow, PyTorch
- Visualization: Matplotlib, NetworkX

### 6. **Standards and Guidelines**
- IETF RFCs (SMTP, DKIM, SPF)
- NIST Cybersecurity Framework
- Industry reports (APWG, Verizon DBIR)

### 7. **Web Resources**
- VirusTotal API
- Google Safe Browsing
- Security awareness resources

---

## Alternative Citation Styles

If your institution requires a different citation style, you can convert the references:

### IEEE Style
- Use citation numbers: [1], [2], etc.
- Tool: Use Zotero/Mendeley to auto-convert

### MLA Style
- Emphasizes author-page format
- Tool: Import BibTeX into Zotero, export as MLA

### Chicago Style
- Uses footnotes or author-date
- Tool: Import into EndNote, change style

### Harvard Style
- Similar to APA but with minor differences
- Tool: Most reference managers support Harvard

---

## Online Conversion Tools

If you need to convert between formats:

1. **BibTeX to APA/MLA/Chicago:**
   - https://www.bibtex.com/c/bibtex-format-converter/
   - https://www.doi2bib.org/

2. **DOI to Citation:**
   - https://www.crossref.org/
   - Enter DOI, get formatted citation

3. **Reference Managers:**
   - Zotero (Free): https://www.zotero.org/
   - Mendeley (Free): https://www.mendeley.com/
   - EndNote (Paid): https://endnote.com/

---

## Tips for Thesis Writing

### 1. **Organize References by Chapter**
Create separate sections for:
- Introduction references
- Literature review references
- Methodology references
- Results/Discussion references

### 2. **Keep Track of Citations**
- Use a spreadsheet to track which sources you've cited
- Note the chapter/section where each source is used
- Verify all in-text citations have corresponding references

### 3. **Check for Consistency**
- All authors' names spelled correctly
- All DOIs/URLs working
- Publication years accurate
- Journal names consistent

### 4. **Common Mistakes to Avoid**
- Missing page numbers for book chapters
- Inconsistent capitalization
- Missing DOIs when available
- Outdated URLs
- Mixing citation styles

### 5. **Verification Checklist**
- [ ] Every in-text citation has a reference entry
- [ ] Every reference entry is cited in text
- [ ] All references are alphabetically ordered
- [ ] Formatting is consistent throughout
- [ ] All URLs are accessible
- [ ] DOIs are included where available

---

## Quick Start: Most Common Citations

Here are the most frequently cited sources for phishing research:

1. **Phishing Surveys/Reviews:**
   - Khonji et al. (2013) - Comprehensive phishing detection survey
   - Chiew et al. (2018) - Types and vectors of phishing
   - Aleroud & Zhou (2017) - Phishing environments and countermeasures

2. **Machine Learning Foundations:**
   - Breiman (2001) - Random Forests
   - Cortes & Vapnik (1995) - Support Vector Machines
   - Chen & Guestrin (2016) - XGBoost

3. **Deep Learning:**
   - LeCun et al. (2015) - Deep learning overview
   - Goodfellow et al. (2016) - Deep learning textbook

4. **Phishing Detection Methods:**
   - Fette et al. (2007) - Learning to detect phishing emails
   - Ma et al. (2009) - URL-based detection
   - Xiang et al. (2011) - CANTINA+

5. **Explainability:**
   - Ribeiro et al. (2016) - LIME
   - Lundberg & Lee (2017) - SHAP

6. **Datasets:**
   - Klimt & Yang (2004) - Enron corpus
   - Nazario (2009) - Phishing corpus

---

## Contact and Support

If you need help with:
- **Format conversion**: Use online tools or reference managers
- **Missing references**: Check original sources or add manually
- **Custom citation style**: Consult your institution's style guide
- **Technical issues**: Refer to LaTeX/BibTeX documentation

---

## Updates and Maintenance

**Last Updated**: November 15, 2024

**Maintenance Notes:**
- Check URLs annually for broken links
- Update software library versions if citing specific versions
- Add new references as research progresses
- Verify DOIs remain accessible

**Version History:**
- v1.0 (2024-11-15): Initial comprehensive reference list
  - 70+ academic sources
  - 20+ software/tool citations
  - 10+ dataset references
  - Standards and guidelines included

---

## License and Attribution

These references are compiled from publicly available academic sources. When using:
- Always cite the original authors
- Follow your institution's academic integrity guidelines
- Verify information before inclusion in your thesis
- Update with most recent versions when available

**Recommended Citation for This Reference List:**
```
Phishing Risk Detection Project. (2024). Comprehensive reference 
bibliography for phishing detection research [Reference list]. 
Retrieved from /docs/REFERENCES.md
```

---

*For questions about specific citations or to report errors, please update the reference files directly or consult with your thesis supervisor.*
