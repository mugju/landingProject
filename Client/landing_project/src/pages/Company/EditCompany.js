import React, {useEffect, useState} from 'react';
import {Box, IconButton, Button, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

export default function EditCompany({ row, closeModal }) {
    const clickSave = () => {
        // submit 함수 추가하기
        closeModal();
        // 저장되었다는 응답 받으면 배너 띄우기
    }
    const clickDelete = () => {
        // alert 띄워서 확인해주기
        // submit 함수 추가하기

        // 삭제되었다는 응답 받으면 배너 띄우기
    }
    return (
        <>
            <div className="modalInnerContainer">
                <div>Name</div>
                <div>:</div>

                <div>{row.com_uid}</div>
                {/* <TextField
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
                    /> */}
                <div className="saveBtn">
                    <Button variant="contained" onClick={() => clickSave()}>Save</Button>
                </div>
            </div>
        </>
    )
}

