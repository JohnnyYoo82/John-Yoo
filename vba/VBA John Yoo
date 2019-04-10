Sub MultiYearStock()

Dim WS As Worksheet
     
For Each WS In ActiveWorkbook.Worksheets
WS.Activate

'variables
Dim Ticker As String
Dim StockVolume As Double
Dim YearOpen As Double
Dim YearClose As Double
Dim YearChange As Double
Dim PercentChange As Double
Dim RowReference As Long
Dim i As Long


' Initial values
StockVolume = 0
RowReference = 2
YearOpen = Cells(2, 3).Value

     
' Headers
Range("J1").Value = "Ticker"
Range("K1").Value = "Yearly Change"
Range("L1").Value = "Percent Change"
Range("M1").Value = "Total Stock Volume"

' Headers for Hard
Range("P1").Value = "Ticker"
Range("Q1").Value = "Value"
        
Range("O2").Value = "Greatest % Increase"
Range("O3").Value = "Greatest % Decrease"
Range("O4").Value = "Greatest Total Volume"

        
' VBA last row function
LastRow = WS.Cells(Rows.Count, 1).End(xlUp).Row
        
        
' Loop for Moderate
    For i = 2 To LastRow
                   
                ' Ticker, yearly change and total stock volume calculated and displayed
                If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then
                    Ticker = Cells(i, 1).Value
                    Cells(RowReference, 10).Value = Ticker
                    YearClose = Cells(i, 6).Value
                    YearChange = YearClose - YearOpen
                    Cells(RowReference, 11).Value = YearChange
                    StockVolume = StockVolume + Cells(i, 7).Value
                    Cells(RowReference, 13).Value = StockVolume
                
                                                                                              
                        ' color scheme heatmap
                        If YearChange < 0 Then
                            Cells(RowReference, 11).Interior.ColorIndex = 3
                        ElseIf YearChange > 0 Then
                            Cells(RowReference, 11).Interior.ColorIndex = 4
                        End If
                        
                      
                      ' Loop to produce percent change in ticker price
                        If YearOpen = 0 And YearClose = 0 Then
                            PercentChange = 0
                        ElseIf YearOpen = 0 And YearClose <> 0 Then
                            PercentChange = 1
                        Else
                            PercentChange = YearChange / YearOpen
                            Cells(RowReference, 12).Value = PercentChange
                            Cells(RowReference, 12).NumberFormat = "0.00%"
                        End If

                        
                    RowReference = RowReference + 1
                    StockVolume = 0
                    YearOpen = Cells(i + 1, 3).Value
                    
                Else
                    StockVolume = StockVolume + Cells(i, 7).Value
                End If
    Next i

    Columns("A:Q").EntireColumn.AutoFit
           
    Next WS
            

End Sub
