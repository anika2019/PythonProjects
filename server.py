from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import List
from pydantic import BaseModel
import db_helper

# run with: uvicorn server:app --reload

app = FastAPI() 

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}

@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expenses_by_date(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")
    total = 0.0
    total = sum([row['total_amount'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total_amount']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total_amount'],
            "percentage": percentage
        }

    return breakdown
    




@app.post("/analytics/monthly/")
def analytics_by_month(date_range: DateRange):
    """
    Fetch expenses from database grouped by month and return analytics data
    with total amount and percentage breakdown for each month.
    """
    from collections import defaultdict
    from datetime import datetime
    
    data = db_helper.fetch_expenses_by_date(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")
    
    # Group expenses by month
    monthly_data = defaultdict(float)
    
    # Fetch detailed data to group by month
    connection = db_helper.get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT DATE_FORMAT(expense_date, '%Y-%m') as month, 
                       SUM(amount) as total_amount 
                FROM expenses 
                WHERE expense_date BETWEEN %s AND %s 
                GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
                ORDER BY month
            """
            cursor.execute(query, (date_range.start_date, date_range.end_date))
            monthly_records = cursor.fetchall()
            
            for record in monthly_records:
                monthly_data[record['month']] = record['total_amount']
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch monthly analytics: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    
    # Calculate total for percentage calculation
    total = sum(monthly_data.values())
    
    # Build response with percentage breakdown
    breakdown = {}
    for month, amount in monthly_data.items():
        percentage = (amount / total) * 100 if total != 0 else 0
        breakdown[month] = {
            "total": amount,
            "percentage": percentage
        }
    
    return breakdown


@app.get("/expenses/{expense_date}", response_model=list[dict])
def fetch_expenses_by_date(expense_date: date):
    # Logic to fetch expenses by date
    expenses = db_helper.fetch_expenses_by_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses