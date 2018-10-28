from datetime import date, datetime, timedelta


def get_chart_date_labels():
    date_labels = []
    today = date.today()
    for i in range(7):
        day = today - timedelta(days=i)
        date_labels.insert(0, str(day))
    date_labels[6] = 'Today'
    date_labels[5] = 'Yesterday'
    return date_labels
