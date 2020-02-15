export interface Race {
    id: number;
    name: string;
    date: string;
    hobby: Category;
    pro: Category;
    family: Category;
}

export interface Category {
    participants: number;
}
