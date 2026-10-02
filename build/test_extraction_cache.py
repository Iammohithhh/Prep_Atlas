"""Verify interrupted writes preserve the last complete OCR checkpoint."""
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
from extract_sources import read_cache, write_json_atomic

with tempfile.TemporaryDirectory(prefix='prep-cache-check-') as directory:
    path = Path(directory)/'record.json'
    original = {'file':'question.jpg','text':'previous complete transcription'}
    write_json_atomic(path, original)
    assert read_cache(path,'question.jpg') == original
    assert read_cache(path,'other.jpg') is None
    normal_write = Path.write_text
    def interrupt_write(target, content, **kwargs):
        normal_write(target, content[:8], **kwargs)
        raise KeyboardInterrupt('simulated interruption')
    with patch.object(Path,'write_text',interrupt_write):
        try: write_json_atomic(path,{'file':'question.jpg','text':'new transcription'})
        except KeyboardInterrupt: pass
        else: raise AssertionError('interruption was not raised')
    assert json.loads(path.read_text(encoding='utf-8')) == original
    assert not list(Path(directory).glob('*.tmp'))
    path.write_text('{truncated',encoding='utf-8')
    assert read_cache(path,'question.jpg') is None
    write_json_atomic(path,original)
    assert read_cache(path,'question.jpg') == original
print('Cache checks passed: interrupted write, corruption, recovery and source identity.')
