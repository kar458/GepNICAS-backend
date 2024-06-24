
    bids_tender_all = [
       {
            'bids_datafolder': bid[0],
            'bids_archivefolder':bid[1]
       
        } for bid in bids_total,
        {
            'tenders_datafolder': tender[0],
            'tenders_archivefolder':tender[1]
        }for tender in tender_total
    ]