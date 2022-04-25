import React, {useEffect, useState} from 'react';
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider, Button, Select, FormControl, InputLabel, MenuItem} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";

const findBankIndex = (bankName, bankList) => {
    let index = 0;
    bankList.map((bank, idx) => {
        if (bankName == bank[idx + 1]){
            index = idx;
        }
    })
    return index
}

export default function EditCompany({ row, bankList, closeModal }) {
    const [select, setSelect] = useState(findBankIndex(row.bank_name, bankList));
    const [inputs, setInputs] = useState({
        "com_uid": row.com_uid,
        "com_name": row.com_name,
        "com_licence_no": row.com_licence_no,
        "com_address": row.com_address,
        "com_contact_no": row.com_contact_no,
        "com_email": row.com_email,
        "com_description": row.com_description,
        "com_joindate": row.com_joindate,
        "com_account_No": row.com_account_No,
        "bank_name": row.bank_name,
    });

    const handleSelect = (event) => {
        const { name, value } = event.target
        setSelect(value);
        setInputs({
            ...inputs,
            [name]: bankList[value][value + 1]
        })
    };

    const handleChange = (event) => {
        const { id, value } = event.target
        setInputs({
            ...inputs,
            [id]: value
        })
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(inputs);


        // axios.post("http://local~~", inputs)
        //     .then((res) => {
        //         console.log(res);
        //         closeModal();
        //     })
    };

    const handleDelete = (uid) => {
        // 확인 모달창 추가

        alert(uid);

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
                <form onSubmit={handleSubmit}>
                    <div className="modalInnerContainer">
                        <div>
                            <div>Name</div>
                            <TextField
                                id="com_name"
                                required
                                label="Required"
                                defaultValue={row.com_name}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>License No.</div>
                            <TextField
                                id="com_licence_no"
                                required
                                label="Required"
                                defaultValue={row.com_licence_no}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Address</div>
                            <TextField
                                id="com_address"
                                required
                                label="Required"
                                defaultValue={row.com_address}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Contact No.</div>
                            <TextField
                                id="com_contact_no"
                                required
                                label="Required"
                                defaultValue={row.com_contact_no}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Email</div>
                            <TextField
                                id="com_email"
                                required
                                label="Required"
                                defaultValue={row.com_email}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Description</div>
                            <TextField
                                id="com_description"
                                required
                                multiline
                                rows={5}
                                label="Required"
                                defaultValue={row.com_description}
                                size="small"
                                onChange={handleChange}
                            />
                        </div>
                        <div className="modalInnerTitle">
                            Company Bank
                        </div>
                        <div>
                            <div>Account No.</div>
                            <TextField
                                id="com_account_no"
                                defaultValue={row.com_account_No}
                                size="small"
                                onChange={handleChange}
                            />
                            <div>Bank Name</div>
                            <div>
                                <FormControl fullWidth>
                                    <Select
                                        name="bank_name"
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
                        <Button
                            variant="contained"
                            color="error"
                            onClick={() => handleDelete(row.com_uid)}
                        >
                            Delete
                        </Button>
                        <Button
                            variant="contained"
                            color="success"
                            type="submit"
                        >
                            Save
                        </Button>
                    </div>
                </form>
            </div>
        </>
    )
}

