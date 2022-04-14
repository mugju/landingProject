import React, {useEffect, useState} from 'react';
import {Box, IconButton, Button, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

export default function ViewCompany({ uid, setModalPage, comName, Licence_No, address, contact_No, email, description }) {
    return (
        <>
            <div className="modalInnerContainer">
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
                    <Button variant="contained" onClick={() => setModalPage('edit')}>Edit</Button>
                </div>
            </div>
        </>
    )
}


