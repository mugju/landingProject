import React, {useEffect, useState} from 'react';
import {Box, IconButton, Button, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

export default function ViewCompany({ row, setModalState }) {

    return (
        <>
            <div style={{backgroundColor:'white'}}>
                <div>{row.com_name}</div>
                <div>{row.com_licence_no}</div>
                <div>{row.com_address}</div>
                <div>{row.com_contact_no}</div>
                <div>{row.com_email}</div>
                <div>{row.com_description}</div>
                <div>{row.bank_name}</div>
                <div>{row.com_account_No}</div>
                <div>
                    <Button variant="contained" onClick={() => setModalState('edit')}>Edit</Button>
                </div>
            </div>
            {/* <div className="modalInnerContainer">
                <div>Name</div>
                <div>:</div>
                <div>{comName}</div>
                <div>License No.</div>
                <div>:</div>
                <div>{Licence_No}</div>
                <div>Address</div>
                <div>:</div>
                <div>{address}</div>
                <div>Contact No.</div>
                <div>:</div>
                <div>{contact_No}</div>
                <div>Email</div>
                <div>:</div>
                <div>{email}</div>
                <div>Description</div>
                <div>:</div>
                <div>{description}</div>


                <div>
                    <Button variant="contained" onClick={() => setModalState('edit')}>Edit</Button>
                </div>
            </div> */}
        </>
    )
}


