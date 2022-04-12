import React, {useEffect, useState} from 'react';
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

export default function EditCompany({ key, comName, Licence_No, address, contact_No, email, description }) {
    return (
        <>
            <div className="modalInnerContainer">
                <div>Name</div>
                <div>:</div>
                <TextField
                    required
                    label="Required"
                    defaultValue={comName}
                    size="small"
                />
                <div>License No.</div>
                <div>:</div>
                <TextField
                    required
                    label="Required"
                    defaultValue={Licence_No}
                    size="small"
                />
                <div>Address</div>
                <div>:</div>
                <TextField
                    required
                    label="Required"
                    defaultValue={address}
                    size="small"
                />
                <div>Contact No.</div>
                <div>:</div>
                <TextField
                    required
                    label="Required"
                    defaultValue={contact_No}
                    size="small"
                />
                <div>Email</div>
                <div>:</div>
                <TextField
                    required
                    label="Required"
                    defaultValue={email}
                    size="small"
                />
                <div>Description</div>
                <div>:</div>
                <TextField
                    placeholder="MultiLine with rows: 2 and rowsMax: 4"
                    multiline
                    rows={5}
                    maxRows={10}
                    label="Required"
                    defaultValue={description}
                    size="small"
                    />
            </div>
        </>
    )
}

