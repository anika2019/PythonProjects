import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

import db_helper



def test_fetch_summary_by_date():
    # Test with a date that is known to have data
    summary = db_helper.fetch_summary_by_date("2024-08-14")
    assert isinstance(summary, list)
    for item in summary:
        assert 'category' in item
        assert 'total_amount' in item
        assert isinstance(item['total_amount'], (int, float))

    # Test with a date that is known to have no data
    summary_empty = db_helper.fetch_summary_by_date("1900-01-01")
    assert summary_empty == []

if __name__ == "__main__":
    test_fetch_summary_by_date()
    print("All tests passed!")
