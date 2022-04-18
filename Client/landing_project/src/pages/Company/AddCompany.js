import React, {useEffect, useState} from 'react';
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider, Button} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";

export default function AddCompany({ closeModal }) {
    const clickSave = () => {
        // submit 함수 추가하기
        console.log('저장');
        closeModal();
        // 저장되었다는 응답 받으면 배너 띄우기
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
                            size="small"
                        />
                        <div>License No.</div>
                        <TextField
                            required
                            label="Required"
                            size="small"
                        />
                        <div>Address</div>
                        <TextField
                            required
                            label="Required"
                            size="small"
                        />
                        <div>Contact No.</div>
                        <TextField
                            required
                            label="Required"
                            size="small"
                        />
                        <div>Email</div>
                        <TextField
                            required
                            label="Required"
                            size="small"
                        />
                        <div>Description</div>
                        <TextField
                            required
                            multiline
                            rows={5}
                            label="Required"
                            size="small"
                        />
                    </div>
                    <div className="modalInnerTitle">
                        Company Bank
                    </div>
                    <div>
                        <div>Account No.</div>
                        <TextField
                            size="small"
                        />
                        <div>Bank Name</div>
                        <TextField
                            size="small"
                        />
                    </div>
                </div>
                <div className="saveButton">
                    <Button variant="contained" onClick={() => clickSave()}>Save</Button>
                </div>
            </div>
        </>
    )
}