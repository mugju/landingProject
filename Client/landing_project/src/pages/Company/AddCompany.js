import React, {useEffect, useState} from 'react';
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider, Button, Select, FormControl, InputLabel, MenuItem} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import { useFormControl } from '@mui/material/FormControl';

export default function AddCompany({ closeModal, bankList }) {
    const [select, setSelect] = useState(0);

    const clickSave = () => {
        // submit 함수 추가하기
        console.log('저장');
        
        // text field 값 받아오기

        // 값 다 받아와서 submit 하는 방식은?

        closeModal();
        // 저장되었다는 응답 받으면 배너 띄우기
    }

    const handleSelect = (event: SelectChangeEvent) => {
        setSelect(event.target.value);
        // console.log(event.target.value);
    };

    const handleChange = (event: ChangeEvent) => {
        console.log(event.target.value);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log("submit")
    };


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
                <form onSubmit={handleSubmit}>
                    <div className="modalInnerContainer">
                        <div>
                            <div>Name</div>
                            <TextField
                                required
                                label="Required"
                                size="small"
                                onChange={handleChange}
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

                            <div>
                                <FormControl fullWidth>
                                    <Select
                                        value={select}
                                        onChange={handleSelect}
                                    >
                                        {bankList.map((bank, index) => (
                                            <MenuItem
                                                key={index + 1}
                                                value={index}
                                            >
                                                {bank[index + 1]}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </div>


                        </div>
                    </div>
                    <div className="saveButton">
                        <Button variant="contained" onClick={() => clickSave()}>Save</Button>
                    </div>
                </form>
            </div>
        </>
    )
}