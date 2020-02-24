export interface Race {
    id: number;
    city: string;
    date: string;
    dnf: number;
    dns: number;
    dsq: number;
    finished: number;
    participants: number;
    percentDnf: number;
    percentDns: number;
    hobby: Category;
    pro: Category;
    family?: Category;
}

export interface Category {
    dnf: number;
    dns: number;
    dsq: number;
    finished: number;
    participants: number;
    percentDnf: number;
    percentDns: number;
}
