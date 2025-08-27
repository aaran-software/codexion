!doctype html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Printing Sales Invoice DC</title>
    <style>
        * {
            font-family: Verdana, Arial, sans-serif, Helvetica, Times;
        }
        table {
            width: 100%;
            border: 1px solid black;
            border-collapse: collapse;
        }
        .page-break {
            page-break-after: always;
        }
        .item-c {
            text-align: center;
        }
        .item-r {
            text-align: right;
        }
        .items-l {
            text-align: left;
        }
        .copy {
            font-size: 12px;
            text-align: right;
        }
        .table-0 {
            border: none;
        }
        .table-2, .table-3, .table-4, .table-5 {
            border-top: none;
        }

    /*    table 1 */
        .table-1 {
            border: 1px solid black;
            border-collapse: collapse;
            text-align: center;
        }
        .comp-name {
            font-size: 25px;
            font-family: "Times New Roman", serif;
        }
        .comp-address {
            font-size: 12px;
            font-weight: bold;
            line-height: 1.3;
        }

    /*    table-2    */
        .inv-det1 {
            width: 25%;
            font-size: 10px;
            line-height: .5;
        }
        .label1, .label2 {
        }
        .label2 {
            border-left: 1px solid black;;
        }
    /*    table 3  */
        .bill-head, .ship-head {
            width: 50%;
            border: 1px solid black;
            border-top: none;
            font-size: 12px;
            background-color: lightgray;
            padding: 3px 0;
        }
        .bill-label, .ship-label {
            width: 10%;
            border-left: 1px solid black;
            vertical-align: top;
            font-size: 10px;
            line-height: 1.5;
        }
        .bill-det, .ship-det {
            width: 40%;
            border-left: 1px solid black;
            vertical-align: top;
            font-size: 10px;
            padding-left: 5px;
            line-height: 1.5;
        }
        .bill-address, .ship-address {
            line-height: .4;
        }

    /*   table 4   */
        .data-head {
            font-size: 10px;
            border-bottom: 1px solid black;

        }
        .data-head > th {
            border-left: 1px solid black;
        }
        .head-div {
            border-bottom: 1px solid black;
        }
        .data {
            font-size: 11px;
            text-align: justify-all;
            vertical-align: top;
        }
        .data > td, .tableSpace > td {
            border-left: 1px solid black;
            height: 40px;
        }
        .subtotal > td {
            font-size: 11px;
            font-weight: bold;
            border: 1px solid black;
            padding: 5px 1px;
        }
    /*    table 5   */
        .total {
            font-size: 10px;
        }
        .total > td {
            border-left: 1px solid black;
            line-height: 1;
        }
        .tot {
            border: 1px solid black;
        }
        .rupees {
            font-size: 10px;
            padding: 5px 1px;
        }
        .sign {
            border: 1px solid black;
        }
        .sign > td {
            font-size: 10px;
            padding: 1px 1px 40px 1px;
            vertical-align: top;
        }
        .auth {
            font-weight: bold;
            font-family: "Times New Roman", serif;
        }
        .other {
            font-size: 8px;
            line-break: normal;
            line-height: .3;
        }

    </style>
</head>
<body>
<!-- Original Copy -->
    <table class="table-0">
        <tr class="copy">
            <td><div>Original Copy&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
        </tr>
    </table>
    <table class="table-1">
        <tr><td class="comp-name">{{$cmp->get('company_name')}}</td></tr>
        <tr class="comp-address"><td>{{$cmp->get('address_1')}},</td></tr>
        <tr class="comp-address"><td>{{$cmp->get('address_1')}},&nbsp;{{$cmp->get('city')}},&nbsp;{{$cmp->get('state')}}</td></tr>
        <tr class="comp-address"><td>{{$cmp->get('contact')}} - {{$cmp->get('email')}}</td></tr>
    </table>
    <table class="table-2">
        <tr>
            <td class="inv-det1 label1">
                <p>&nbsp;&nbsp;GSTIN NO </p>
                <p>&nbsp;&nbsp;Invoice No </p>
                <p>&nbsp;&nbsp;Invoice Date</p>
            </td>
            <td class="inv-det1 ">
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$cmp->get('gst')}}</p>
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_no}}</p>
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_date ?date('d-m-Y', strtotime($obj->invoice_date)):''}}</p>
            </td>
            <td class="inv-det1 label2 ">
                <p>&nbsp;&nbsp;Trans. Mode</p>
                <p>&nbsp;&nbsp;Vehicle No</p>
                <p>&nbsp;&nbsp;Date & Time of Supply</p>
                <p>&nbsp;&nbsp;Place of Supply</p>
            </td>
            <td class="inv-det1">
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
                <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            </td>
        </tr>
    </table>
    <table class="table-3">
        <tr>
            <th colspan="2" class="bill-head">Customer Name & Address (Billed To)</th>
            <th colspan="2" class="ship-head">Customer Name & Address (Shipped To)</th>
        </tr>
        <tr>
            <td class="bill-label">&nbsp;Name</td>
            <td class="bill-det">{{$obj->contact_name}}</td>
            <td class="ship-label">&nbsp;Name</td>
            <td class="ship-det">{{$obj->contact_name}}</td>
        </tr>
        <tr>
            <td class="bill-label">&nbsp;Address</td>
            <td class="bill-det bill-address">
                <p>{{$billing_address->get('address_1')}}</p>
                <p>{{$billing_address->get('address_2')}}</p>
                <p>{{$billing_address->get('address_3')}}</p>
            </td>
            <td class="ship-label">&nbsp;Address</td>
            <td class="ship-det ship-address">
                <p>{{$shipping_address->get('address_1')}}</p>
                <p>{{$shipping_address->get('address_2')}}</p>
                <p>{{$shipping_address->get('address_3')}}</p>
            </td>
        </tr>
        <tr>
            <td class="bill-label">&nbsp;Phone</td>
            <td class="bill-det">{{$billing_address->get('contact')}}</td>
            <td class="ship-label">&nbsp;Phone</td>
            <td class="ship-det">{{$shipping_address->get('contact')}}</td>
        </tr>
        <tr>
            <td class="bill-label">&nbsp;GSTIN NO</td>
            <td class="bill-det">{{$billing_address->get('gstContact')}}</td>
            <td class="ship-label">&nbsp;GSTIN NO</td>
            <td class="ship-det">{{$shipping_address->get('gstContact')}}</td>
        </tr>
    </table>
    <table class="table-4">
        <tr class="data-head">
            <th width="5%" rowspan="2">S No</th>
            <th width="8%" rowspan="2">HSN Code</th>
            <th width="22%" rowspan="2">Description of Goods</th>
            <th width="5%" rowspan="2">Size</th>
            <th width="5%" rowspan="2">Qty</th>
            <th width="5%" rowspan="2">Rate</th>
            <th width="11%" rowspan="2">Taxable Value</th>
            <th width="13%" colspan="2" class="head-div">CGST</th>
            <th width="13%" colspan="2" class="head-div">SGST</th>
            <th width="13%" colspan="2" class="head-div">IGST</th>
        </tr>
        <tr class="data-head">
            <th width="4%">(%)</th>
            <th width="9%">Amount</th>
            <th width="4%">(%)</th>
            <th width="9%">Amount</th>
            <th width="4%">(%)</th>
            <th width="9%">Amount</th>
        </tr>
        @php
            $gstPercent = 0;
        @endphp
        @if($obj->sales_type==0)
        @foreach($list as $index => $row)
        <tr class="data">
            <td class="item-c">{{$index+1}}</td>
            <td>{{$row['hsncode']}}</td>
            <td>
                @if($row['description'])
                    {{$row['product_name'].' - '.$row['description']}}
                @else
                    {{$row['product_name']}}
                @endif
            </td>
            <td class="item-c">{{$row['size_name']}}</td>
            <td class="item-c">{{$row['qty']+0}}</td>
            <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
            <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
            <td class="item-c">{{$row['gst_percent']}}</td>
            <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
            <td class="item-c">{{$row['gst_percent']}}</td>
            <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        @endforeach
        @else
        @foreach($list as $index => $row)
        <tr class="data">
            <td class="item-c">{{$index+1}}</td>
            <td>{{$row['hsncode']}}</td>
            <td>
                @if($row['description'])
                    {{$row['product_name'].' - '.$row['description']}}
                @else
                    {{$row['product_name']}}
                @endif
            </td>
            <td class="item-c">{{$row['size_name']}}</td>
            <td class="item-c">{{$row['qty']+0}}</td>
            <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
            <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td class="item-c">{{$row['gst_percent']*2}}</td>
            <td class="item-r">{{number_format($row['gst_amount'],2,'.','')}}</td>
        </tr>
        @endforeach
            @php
                $gstPercent = $row['gst_percent'];
            @endphp
        @endif
        {{-- Spacing  --}}
        @for($i = 0; $i < 10-$list->count(); $i++)
            <tr class="tableSpace">

                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
        @endfor

        <tr class="subtotal">
            <td class="item-r" colspan="4">Total Packages&nbsp;&nbsp;</td>
            <td class="item-c">{{$obj->total_qty+0}}</td>
            <td>&nbsp;</td>
            <td class="item-r">{{number_format($obj->total_taxable,2,'.','')}}</td>
            <td>&nbsp;</td>
            <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td>&nbsp;</td>
            <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            @if($obj->sales_type==0)
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            @else
            <td>&nbsp;</td>
            <td class="item-r">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            @endif
        </tr>
    </table>
<table class="table-5">
    @if($obj->sales_type==0)
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @else
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;0.00</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @endif
    <tr>
        <td class="rupees" colspan="6" ><span>Amount (in words)</span>&nbsp;&nbsp;&nbsp;<span><b>{{$rupees}}Only</b></span></td>
    </tr>
    <tr class="sign">
        <td colspan="3"><div class="item-c">
                Received the above goods in Good condition
            </div></td>
        <td colspan="3" style="border-left: 1px solid black">
            <div class="item-c">
                <span>for</span>&nbsp;&nbsp;&nbsp;<span class="auth">{{$cmp->get('company_name')}}</span>
            </div>
        </td>
    </tr>
</table>
    <div class="page-break"></div>

<!-- Duplicate Copy -->
<table class="table-0">
    <tr class="copy">
        <td><div>Duplicate Copy&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
    </tr>
</table>
<table class="table-1">
    <tr><td class="comp-name">{{$cmp->get('company_name')}}</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('address_1')}},</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('address_1')}},&nbsp;{{$cmp->get('city')}},&nbsp;{{$cmp->get('state')}}</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('contact')}} - {{$cmp->get('email')}}</td></tr>
</table>
<table class="table-2">
    <tr>
        <td class="inv-det1 label1">
            <p>&nbsp;&nbsp;GSTIN NO </p>
            <p>&nbsp;&nbsp;Invoice No </p>
            <p>&nbsp;&nbsp;Invoice Date</p>
        </td>
        <td class="inv-det1 ">
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$cmp->get('gst')}}</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_no}}</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_date ?date('d-m-Y', strtotime($obj->invoice_date)):''}}</p>
        </td>
        <td class="inv-det1 label2 ">
            <p>&nbsp;&nbsp;Trans. Mode</p>
            <p>&nbsp;&nbsp;Vehicle No</p>
            <p>&nbsp;&nbsp;Date & Time of Supply</p>
            <p>&nbsp;&nbsp;Place of Supply</p>
        </td>
        <td class="inv-det1">
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
        </td>
    </tr>
</table>
<table class="table-3">
    <tr>
        <th colspan="2" class="bill-head">Customer Name & Address (Billed To)</th>
        <th colspan="2" class="ship-head">Customer Name & Address (Shipped To)</th>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Name</td>
        <td class="bill-det">{{$obj->contact_name}}</td>
        <td class="ship-label">&nbsp;Name</td>
        <td class="ship-det">{{$obj->contact_name}}</td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Address</td>
        <td class="bill-det bill-address">
            <p>{{$billing_address->get('address_1')}}</p>
            <p>{{$billing_address->get('address_2')}}</p>
            <p>{{$billing_address->get('address_3')}}</p>
        </td>
        <td class="ship-label">&nbsp;Address</td>
        <td class="ship-det ship-address">
            <p>{{$shipping_address->get('address_1')}}</p>
            <p>{{$shipping_address->get('address_2')}}</p>
            <p>{{$shipping_address->get('address_3')}}</p>
        </td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Phone</td>
        <td class="bill-det">{{$billing_address->get('contact')}}</td>
        <td class="ship-label">&nbsp;Phone</td>
        <td class="ship-det">{{$shipping_address->get('contact')}}</td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;GSTIN NO</td>
        <td class="bill-det">{{$billing_address->get('gstContact')}}</td>
        <td class="ship-label">&nbsp;GSTIN NO</td>
        <td class="ship-det">{{$shipping_address->get('gstContact')}}</td>
    </tr>
</table>
<table class="table-4">
    <tr class="data-head">
        <th width="5%" rowspan="2">S No</th>
        <th width="8%" rowspan="2">HSN Code</th>
        <th width="22%" rowspan="2">Description of Goods</th>
        <th width="5%" rowspan="2">Size</th>
        <th width="5%" rowspan="2">Qty</th>
        <th width="5%" rowspan="2">Rate</th>
        <th width="11%" rowspan="2">Taxable Value</th>
        <th width="13%" colspan="2" class="head-div">CGST</th>
        <th width="13%" colspan="2" class="head-div">SGST</th>
        <th width="13%" colspan="2" class="head-div">IGST</th>
    </tr>
    <tr class="data-head">
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
    </tr>
    @php
        $gstPercent = 0;
    @endphp
    @if($obj->sales_type==0)
        @foreach($list as $index => $row)
            <tr class="data">
                <td class="item-c">{{$index+1}}</td>
                <td>{{$row['hsncode']}}</td>
                <td>
                    @if($row['description'])
                        {{$row['product_name'].' - '.$row['description']}}
                    @else
                        {{$row['product_name']}}
                    @endif
                </td>
                <td class="item-c">{{$row['size_name']}}</td>
                <td class="item-c">{{$row['qty']+0}}</td>
                <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
                <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
                <td class="item-c">{{$row['gst_percent']}}</td>
                <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
                <td class="item-c">{{$row['gst_percent']}}</td>
                <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
        @endforeach
    @else
        @foreach($list as $index => $row)
            <tr class="data">
                <td class="item-c">{{$index+1}}</td>
                <td>{{$row['hsncode']}}</td>
                <td>
                    @if($row['description'])
                        {{$row['product_name'].' - '.$row['description']}}
                    @else
                        {{$row['product_name']}}
                    @endif
                </td>
                <td class="item-c">{{$row['size_name']}}</td>
                <td class="item-c">{{$row['qty']+0}}</td>
                <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
                <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td class="item-c">{{$row['gst_percent']*2}}</td>
                <td class="item-r">{{number_format($row['gst_amount'],2,'.','')}}</td>
            </tr>
        @endforeach
        @php
            $gstPercent = $row['gst_percent'];
        @endphp
    @endif
    {{-- Spacing  --}}
    @for($i = 0; $i < 10-$list->count(); $i++)
        <tr class="tableSpace">

            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
    @endfor

    <tr class="subtotal">
        <td class="item-r" colspan="4">Total Packages&nbsp;&nbsp;</td>
        <td class="item-c">{{$obj->total_qty+0}}</td>
        <td>&nbsp;</td>
        <td class="item-r">{{number_format($obj->total_taxable,2,'.','')}}</td>
        <td>&nbsp;</td>
        <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
        <td>&nbsp;</td>
        <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
        @if($obj->sales_type==0)
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        @else
            <td>&nbsp;</td>
            <td class="item-r">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
        @endif
    </tr>
</table>
<table class="table-5">
    @if($obj->sales_type==0)
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @else
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;0.00</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @endif
    <tr>
        <td class="rupees" colspan="6" ><span>Amount (in words)</span>&nbsp;&nbsp;&nbsp;<span><b>{{$rupees}}Only</b></span></td>
    </tr>
    <tr class="sign">
        <td colspan="3"><div class="item-c">
                Received the above goods in Good condition
            </div></td>
        <td colspan="3" style="border-left: 1px solid black">
            <div class="item-c">
                <span>for</span>&nbsp;&nbsp;&nbsp;<span class="auth">{{$cmp->get('company_name')}}</span>
            </div>
        </td>
    </tr>
</table>
<div class="page-break"></div>

<!-- Triplicate Copy -->
<table class="table-0">
    <tr class="copy">
        <td><div>Triplicate Copy&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
    </tr>
</table>
<table class="table-1">
    <tr><td class="comp-name">{{$cmp->get('company_name')}}</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('address_1')}},</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('address_1')}},&nbsp;{{$cmp->get('city')}},&nbsp;{{$cmp->get('state')}}</td></tr>
    <tr class="comp-address"><td>{{$cmp->get('contact')}} - {{$cmp->get('email')}}</td></tr>
</table>
<table class="table-2">
    <tr>
        <td class="inv-det1 label1">
            <p>&nbsp;&nbsp;GSTIN NO </p>
            <p>&nbsp;&nbsp;Invoice No </p>
            <p>&nbsp;&nbsp;Invoice Date</p>
        </td>
        <td class="inv-det1 ">
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$cmp->get('gst')}}</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_no}}</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;{{$obj->invoice_date ?date('d-m-Y', strtotime($obj->invoice_date)):''}}</p>
        </td>
        <td class="inv-det1 label2 ">
            <p>&nbsp;&nbsp;Trans. Mode</p>
            <p>&nbsp;&nbsp;Vehicle No</p>
            <p>&nbsp;&nbsp;Date & Time of Supply</p>
            <p>&nbsp;&nbsp;Place of Supply</p>
        </td>
        <td class="inv-det1">
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
            <p>&nbsp;:&nbsp;&nbsp;&nbsp;</p>
        </td>
    </tr>
</table>
<table class="table-3">
    <tr>
        <th colspan="2" class="bill-head">Customer Name & Address (Billed To)</th>
        <th colspan="2" class="ship-head">Customer Name & Address (Shipped To)</th>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Name</td>
        <td class="bill-det">{{$obj->contact_name}}</td>
        <td class="ship-label">&nbsp;Name</td>
        <td class="ship-det">{{$obj->contact_name}}</td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Address</td>
        <td class="bill-det bill-address">
            <p>{{$billing_address->get('address_1')}}</p>
            <p>{{$billing_address->get('address_2')}}</p>
            <p>{{$billing_address->get('address_3')}}</p>
        </td>
        <td class="ship-label">&nbsp;Address</td>
        <td class="ship-det ship-address">
            <p>{{$shipping_address->get('address_1')}}</p>
            <p>{{$shipping_address->get('address_2')}}</p>
            <p>{{$shipping_address->get('address_3')}}</p>
        </td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;Phone</td>
        <td class="bill-det">{{$billing_address->get('contact')}}</td>
        <td class="ship-label">&nbsp;Phone</td>
        <td class="ship-det">{{$shipping_address->get('contact')}}</td>
    </tr>
    <tr>
        <td class="bill-label">&nbsp;GSTIN NO</td>
        <td class="bill-det">{{$billing_address->get('gstContact')}}</td>
        <td class="ship-label">&nbsp;GSTIN NO</td>
        <td class="ship-det">{{$shipping_address->get('gstContact')}}</td>
    </tr>
</table>
<table class="table-4">
    <tr class="data-head">
        <th width="5%" rowspan="2">S No</th>
        <th width="8%" rowspan="2">HSN Code</th>
        <th width="22%" rowspan="2">Description of Goods</th>
        <th width="5%" rowspan="2">Size</th>
        <th width="5%" rowspan="2">Qty</th>
        <th width="5%" rowspan="2">Rate</th>
        <th width="11%" rowspan="2">Taxable Value</th>
        <th width="13%" colspan="2" class="head-div">CGST</th>
        <th width="13%" colspan="2" class="head-div">SGST</th>
        <th width="13%" colspan="2" class="head-div">IGST</th>
    </tr>
    <tr class="data-head">
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
        <th width="4%">(%)</th>
        <th width="9%">Amount</th>
    </tr>
    @php
        $gstPercent = 0;
    @endphp
    @if($obj->sales_type==0)
        @foreach($list as $index => $row)
            <tr class="data">
                <td class="item-c">{{$index+1}}</td>
                <td>{{$row['hsncode']}}</td>
                <td>
                    @if($row['description'])
                        {{$row['product_name'].' - '.$row['description']}}
                    @else
                        {{$row['product_name']}}
                    @endif
                </td>
                <td class="item-c">{{$row['size_name']}}</td>
                <td class="item-c">{{$row['qty']+0}}</td>
                <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
                <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
                <td class="item-c">{{$row['gst_percent']}}</td>
                <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
                <td class="item-c">{{$row['gst_percent']}}</td>
                <td class="item-r">{{number_format($row['gst_amount']/2,2,'.','')}}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
        @endforeach
    @else
        @foreach($list as $index => $row)
            <tr class="data">
                <td class="item-c">{{$index+1}}</td>
                <td>{{$row['hsncode']}}</td>
                <td>
                    @if($row['description'])
                        {{$row['product_name'].' - '.$row['description']}}
                    @else
                        {{$row['product_name']}}
                    @endif
                </td>
                <td class="item-c">{{$row['size_name']}}</td>
                <td class="item-c">{{$row['qty']+0}}</td>
                <td class="item-r">{{number_format($row['price'],2,'.','')}}</td>
                <td class="item-r">{{number_format($row['qty']*$row['price'],2,'.','')}}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td class="item-c">{{$row['gst_percent']*2}}</td>
                <td class="item-r">{{number_format($row['gst_amount'],2,'.','')}}</td>
            </tr>
        @endforeach
        @php
            $gstPercent = $row['gst_percent'];
        @endphp
    @endif
    {{-- Spacing  --}}
    @for($i = 0; $i < 10-$list->count(); $i++)
        <tr class="tableSpace">

            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
    @endfor

    <tr class="subtotal">
        <td class="item-r" colspan="4">Total Packages&nbsp;&nbsp;</td>
        <td class="item-c">{{$obj->total_qty+0}}</td>
        <td>&nbsp;</td>
        <td class="item-r">{{number_format($obj->total_taxable,2,'.','')}}</td>
        <td>&nbsp;</td>
        <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
        <td>&nbsp;</td>
        <td class="item-r">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
        @if($obj->sales_type==0)
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        @else
            <td>&nbsp;</td>
            <td class="item-r">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
        @endif
    </tr>
</table>
<table class="table-5">
    @if($obj->sales_type==0)
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst/2,2,'.','')}}</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @else
        <tr class="total">
            <td class="bank" width="13%" rowspan="5">
                <p>&nbsp;<b>Bank Details</b></p>
                <p>&nbsp;Bank Name</p>
                <p>&nbsp;Account Name</p>
                <p>&nbsp;Account No</p>
                <p>&nbsp;IFSC Code</p>
                <p>&nbsp;Branch</p>
            </td>
            <td class="bank" width="22%" rowspan="5">
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('bank')}}</p>
                <p>&nbsp;</p>
                <p>&nbsp;{{$cmp->get('acc_no')}}</p>
                <p>&nbsp;{{$cmp->get('ifsc_code')}}</p>
                <p>&nbsp;{{$cmp->get('branch')}}</p>
            </td>
            <td>&nbsp;</td>
            <td style="border-left: none;">&nbsp;</td>
            @if($obj->additional!=0)
                <td >&nbsp;Freight Charges&nbsp;:&nbsp;<span class="other">(&nbsp;{{ $obj->ledger_name }}&nbsp;)</span></td>
                <td class="item-r">&nbsp;{{ number_format($obj->additional,2,'.','') }}</td>
            @else
                <td>&nbsp;Freight Charges</td>
                <td class="item-r">&nbsp;0.00</td>
            @endif
        </tr>
        <tr class="total tot">
            <td width="15%">&nbsp;Total CGST</td>
            <td class="item-r" style="border-left: none;" width="11%">&nbsp;0.00</td>
            <td width="26%">&nbsp;Loading & Packing Charges</td>
            <td class="item-r" width="13%">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Toatal SGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;0.00</td>
            <td>&nbsp;Insurance Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot">
            <td>&nbsp;Total IGST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Other Charges</td>
            <td class="item-r">&nbsp;0.00</td>
        </tr>
        <tr class="total tot " style="font-weight: bold">
            <td>&nbsp;Total GST</td>
            <td class="item-r" style="border-left: none;">&nbsp;{{number_format($obj->total_gst,2,'.','')}}</td>
            <td>&nbsp;Grand Total</td>
            <td class="item-r">&nbsp;{{number_format($obj->grand_total,2,'.','')}}</td>
        </tr>
    @endif
    <tr>
        <td class="rupees" colspan="6" ><span>Amount (in words)</span>&nbsp;&nbsp;&nbsp;<span><b>{{$rupees}}Only</b></span></td>
    </tr>
    <tr class="sign">
        <td colspan="3"><div class="item-c">
                Received the above goods in Good condition
            </div></td>
        <td colspan="3" style="border-left: 1px solid black">
            <div class="item-c">
                <span>for</span>&nbsp;&nbsp;&nbsp;<span class="auth">{{$cmp->get('company_name')}}</span>
            </div>
        </td>
    </tr>
</table>

</body>
</html>
