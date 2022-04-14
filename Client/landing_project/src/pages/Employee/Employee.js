import React, {useEffect, useState} from 'react';


import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Button from "@mui/material/Button";
import {Box, IconButton, Modal, Typography, TextField, Tooltip, Divider} from "@mui/material";

import ClearIcon from '@mui/icons-material/Clear';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

import styles from './Employee.module.css'

export default function Employee() {
    const [rows, setRows] = useState([
        {
            "emp_uid": 0,
            "emp_name": "홍길동0",
            "emp_joindate": "2022-01-01",
            "emp_phone": "01012345666",
            "emp_address": "서울특별시서울특별시 서울특별시서울특별시서울특별시서울특별시서울특별시 서울특별시서울특별시서울특별시서울특별시서울특별시서울특별시서울특별시 서울특별시서울특별시서울특별시서울특별시서울특별시서울특별시서울특별시",
            "emp_add_on": "2022-02-02"
        },
        {
            "emp_uid": 0,
            "emp_name": "홍길동0",
            "emp_joindate": "2022-01-01",
            "emp_phone": "01012345666",
            "emp_address": "서울특별시",
            "emp_add_on": "2022-02-02"
        },
        {
            "emp_uid": 0,
            "emp_name": "홍길동0",
            "emp_joindate": "2022-01-01",
            "emp_phone": "01012345666",
            "emp_address": "서울특별시",
            "emp_add_on": "2022-02-02"
        },

    ])

    return (
        <>
            <div className="tableContainer">
                <div className="titleContainer">
                    <div>All Employee Data</div>
                    <div><Button variant="contained" size="medium">Add Company</Button></div>
                </div>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>No.</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Joining Date</TableCell>
                                <TableCell>Phone</TableCell>
                                <TableCell>Address</TableCell>
                                <TableCell>Added On</TableCell>
                                <TableCell>Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.map((row) => (
                                <TableRow
                                    key={row.uid}                                    
                                >
                                    <TableCell component="th" scope="row">
                                        {row.emp_uid}
                                    </TableCell>
                                    <TableCell className={styles.test}>{row.emp_name}</TableCell>
                                    <TableCell>{row.emp_joindate}</TableCell>
                                    <TableCell>{row.emp_phone}</TableCell>
                                    <TableCell><div className="rowContainer">{row.emp_address}</div></TableCell>
                                    <TableCell>{row.emp_add_on}</TableCell>
                                    <TableCell><Button variant="contained" size="small">View</Button></TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>


                </TableContainer>

                <Stack className="pContainer" spacing={2}>
                    <Pagination className="pagination" count={30} color="primary" />
                </Stack>
            </div>
        </>
    )
}