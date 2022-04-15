import React, {useEffect, useState} from 'react';
import {Box, IconButton, Button, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";
import ClearIcon from '@mui/icons-material/Clear';

export default function ViewCompany({ row, setModalState, closeModal }) {

    return (
        <>
            <div className="modalContainer">
                <div className='closeButton'>
                    <Tooltip title="Close">
                        <IconButton onClick={closeModal}>
                            <ClearIcon />
                        </IconButton>
                    </Tooltip>
                </div>
                <div className="modalInnerContainer">
                    <div>
                        <div>Name</div>
                        <div>{row.com_name}</div>
                        <div>License No.</div>
                        <div>{row.com_licence_no}</div>
                        <div>Address</div>
                        <div>{row.com_address}</div>
                        <div>Contact No.</div>
                        <div>{row.com_contact_no}</div>
                        <div>Email</div>
                        <div>{row.com_email}</div>
                        <div>Description</div>
                        <div className="modalDescription">{row.com_description}</div>
                    </div>
                    <div className="modalInnerTitle">
                        Company Bank
                    </div>
                    <div>
                        <div>Account No.</div>
                        <div>{row.bank_name}</div>
                        <div>Bank Name</div>
                        <div>{row.com_account_No}</div>
                    </div>
                </div>
                <div className="editButton">
                    <Button variant="contained" onClick={() => setModalState('edit')}>Edit</Button>
                </div>
            </div>
        </>
    )
}