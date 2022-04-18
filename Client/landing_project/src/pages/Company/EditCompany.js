import React, {useEffect, useState} from 'react';
import {Box, IconButton, Button, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import ClearIcon from "@mui/icons-material/Clear";

export default function EditCompany({ row, closeModal }) {
    const clickSave = () => {
        // submit 함수 추가하기
        console.log('저장');
        closeModal();
        // 저장되었다는 응답 받으면 배너 띄우기
    }
    const clickDelete = () => {
        alert("test");
        // 삭제 확인창
        // submit 함수 추가하기

        // 삭제되었다는 응답 받으면 배너 띄우기
    }
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
                        <TextField
                            required
                            label="Required"
                            defaultValue={row.com_name}
                            size="small"
                        />
                        <div>License No.</div>
                        <TextField
                            required
                            label="Required"
                            defaultValue={row.com_licence_no}
                            size="small"
                        />
                        <div>Address</div>
                        <TextField
                            required
                            label="Required"
                            defaultValue={row.com_address}
                            size="small"
                        />
                        <div>Contact No.</div>
                        <TextField
                            required
                            label="Required"
                            defaultValue={row.com_contact_no}
                            size="small"
                        />
                        <div>Email</div>
                        <TextField
                            required
                            label="Required"
                            defaultValue={row.com_email}
                            size="small"
                        />
                        <div>Description</div>
                        <TextField
                            required
                            multiline
                            rows={5}
                            label="Required"
                            defaultValue={row.com_description}
                            size="small"
                        />
                    </div>
                    <div className="modalInnerTitle">
                        Company Bank
                    </div>
                    <div>
                        <div>Account No.</div>
                        <TextField
                            defaultValue={row.bank_name}
                            size="small"
                        />
                        <div>Bank Name</div>
                        <TextField
                            defaultValue={row.com_account_No}
                            size="small"
                        />
                    </div>
                </div>
                <div className="saveButton">
                    <Button variant="contained" onClick={() => clickDelete()}>Delete</Button>
                    <Button variant="contained" onClick={() => clickSave()}>Save</Button>
                </div>
            </div>
        </>
    )
}

