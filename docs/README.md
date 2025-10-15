# Documentation

This directory contains all documentation for the Read2Me project.

## Files

### User Documentation
- **`USAGE.md`**: Comprehensive usage guide for all components
  - CLI usage examples
  - Library integration patterns
  - Web API documentation
  - Bookshelf integration examples

### Technical Documentation
- **`research/`**: Research notes and technical information
  - `notes.md`: TTS concepts and terminology
  - Technical research on speech synthesis

- **`schema_notes.md`**: Database schema and data structure documentation
  - Filesystem organization
  - JSON schemas
  - PostgreSQL database design

## Documentation Structure

### For Users
1. **Quick Start**: See main README.md in repository root
2. **Detailed Usage**: Read `USAGE.md` for comprehensive examples
3. **API Reference**: Check individual README files in `src/` subdirectories

### For Developers
1. **Architecture**: Review `../CLAUDE.md` for system overview
2. **Module Docs**: Check README files in `src/read2me/*/`
3. **Legacy Systems**: See `../legacy/README.md` for migration info

### For AI/Models
1. **Code Structure**: Each module has detailed README with class/method documentation
2. **Integration Patterns**: USAGE.md contains integration examples
3. **Error Handling**: Documented in individual module READMEs
4. **Data Formats**: Schemas and structures in schema_notes.md

## Additional Resources

### Voice Samples
Available voice samples documented in `USAGE.md` under Configuration section.

### Model Information
TTS model details and configuration in main `CLAUDE.md` file.

### Troubleshooting
Common issues and solutions in `USAGE.md` troubleshooting section.

## Contributing Documentation

When adding new features:

1. **Update Module README**: Add new methods/classes to appropriate `src/read2me/*/README.md`
2. **Update Usage Guide**: Add examples to `USAGE.md`
3. **Update Architecture**: Modify `CLAUDE.md` if architecture changes
4. **API Documentation**: Update API docs in `src/read2me/api/README.md`

## Format Guidelines

- Use clear headings and subheadings
- Include code examples for all features
- Document parameters and return values
- Provide integration examples
- Include error handling patterns
- Add performance considerations where relevant